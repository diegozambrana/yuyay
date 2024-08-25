import logging
import sys

from db.supabase import supabase

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')


def get_pystats_data_from_db(name):
    """
    Get python package data from Supabase
    """
    response = supabase.table('package_python_downloads').select('*').eq('name', name).execute()
    return response


def insert_pystats_data_to_db(name, data, forecast):
    """
    Insert python package data to Supabase
    """
    response = supabase.table('package_python_downloads').insert({
        'name': name,
        'data': data,
        'prediction': forecast
    }).execute()
    return response