import logging
import sys

from db.supabase import supabase

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')


def get_by_symbol(symbol: str):
    """
    Get the Yahoo Finance data by symbol from the database.
    """
    logger.info('Get Yahoo Finance data by symbol')
    logger.info(f"Symbol: {symbol}")
    response = supabase.table('yahoo_finance_data').select('*').eq('symbol', symbol).execute()
    return response


def insert_yahoo_finance(data: dict):
    """
    Insert the Yahoo Finance data into the database.
    """
    logger.info('Insert Yahoo Finance data')
    response = supabase.table("yahoo_finance_data").insert(data).execute()
    logger.info(f"Response: {response}")
    return response


def update_yahoo_finance(symbol: str, data: dict):
    """
    Update the Yahoo Finance data in the database.
    """
    logger.info('Update Yahoo Finance data')
    response = supabase.table("yahoo_finance_data").update(data).eq('symbol', symbol).execute()
    return response