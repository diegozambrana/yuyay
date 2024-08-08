import os
import warnings
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv

warnings.filterwarnings(
    "ignore",
    message="pandas only supports SQLAlchemy connectable.*",
)

load_dotenv()

ENV_VARIABLES = {key: os.getenv(key) for key in os.environ.keys() if key.isupper()}


def db_connection_manager(dbname, user, password, host):
    @contextmanager
    def _get_db(return_cursor=True):
        conn = None
        cursor = None
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
            )
            cursor = conn.cursor()
            if return_cursor:
                yield cursor
            else:
                yield conn
            conn.commit()

        except Exception as e:
            if conn is not None:
                conn.rollback()
            raise Exception(f"An error occurred: {e}")
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

    return _get_db


dev_portal_main_db = db_connection_manager(
    dbname=ENV_VARIABLES.get("DB_NAME"),
    user=ENV_VARIABLES.get("DEV_PORTAL_MAIN_DB_USER"),
    password=ENV_VARIABLES.get("DEV_PORTAL_MAIN_DB_PASSWORD"),
    host=ENV_VARIABLES.get("DB_HOST_MAIN_DB"),
)

dev_portal_dev_db = db_connection_manager(
    dbname=ENV_VARIABLES.get("DB_NAME"),
    user=ENV_VARIABLES.get("DEV_PORTAL_DEV_DB_USER"),
    password=ENV_VARIABLES.get("DEV_PORTAL_DEV_DB_PASSWORD"),
    host=ENV_VARIABLES.get("DB_HOST"),
)

ixchel_db = db_connection_manager(
    dbname=ENV_VARIABLES.get("DB_NAME"),
    user=ENV_VARIABLES.get("IXCHEL_DB_USER"),
    password=ENV_VARIABLES.get("IXCHEL_DB_PASSWORD"),
    host=ENV_VARIABLES.get("DB_HOST"),
)


def _get_db_manager(database: str, cursor: bool):
    if database == "ixchel":
        return ixchel_db(return_cursor=cursor)
    elif database == "dev-main-portal":
        return dev_portal_main_db(return_cursor=cursor)
    elif database == "dev-portal-dev":
        return dev_portal_dev_db(return_cursor=cursor)
    else:
        raise Exception(f"Unknown database: {database}")


class DataBase:
    @staticmethod
    def cursor(database: str):
        return _get_db_manager(database=database, cursor=True)

    @staticmethod
    def conn(database: str):
        return _get_db_manager(database=database, cursor=False)
