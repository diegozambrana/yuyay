import logging
import sys

from db.supabase import supabase
from utils.nixtla import forecast

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')


def get_by_symbol(symbol: str):
    """
    Get the Yahoo Finance data by symbol from the database.
    """
    response = supabase.table('yahoo_finance_data').select('*').eq('symbol', symbol).execute()
    return response


def insert_yahoo_finance(data: dict):
    """
    Insert the Yahoo Finance data into the database.
    """
    response = supabase.table("yahoo_finance_data").insert(data).execute()
    return response


def update_yahoo_finance(symbol: str, data: dict):
    """
    Update the Yahoo Finance data in the database.
    """
    response = supabase.table("yahoo_finance_data").update(data).eq('symbol', symbol).execute()
    return response

def get_latest_data():
    """
    Get the latest Yahoo Finance data from the database.
    """
    response = supabase.table('yahoo_finance_data').select('id, symbol, name').order('updated_at', desc=True).limit(10).execute()
    return response