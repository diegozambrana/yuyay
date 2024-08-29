import logging
import sys

from db.supabase import supabase

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('Tracker DB')


# TRACKER

def get_tracking_list_by_tracker_details_id(tracker_details_id):
    """
    Get all tracker data from Supabase
    """
    response = supabase.table('tracker').select('*').eq('tracker_details_id', tracker_details_id).order("started_at", desc=True).execute()
    return response


def insert_tracker_data(data):
    """
    Insert tracker data to Supabase
    """
    response = supabase.table('tracker').insert(data).execute()
    return response


def get_tracker_data(tracking_id):
    """
    Get tracker data from Supabase
    """
    response = supabase.table('tracker').select('*').eq('tracker_id', tracking_id).execute()
    return response

def delete_tracker_data(tracking_id):
    """
    Delete tracker data from Supabase
    """
    response = supabase.table('tracker').delete().eq('tracker_id', tracking_id).execute()
    return response

def update_tracker_data(tracking_id, data):
    """
    Update tracker data from Supabase
    """
    response = supabase.table('tracker').update(data).eq('tracker_id', tracking_id).execute()
    return response

# TRACKER DETAILS

def get_tracker_details_data():
    """
    Get all tracker details data from Supabase
    """
    response = supabase.table('tracker_details').select('id, name, code, description').execute()
    return response


def get_tracker_details_by_code(code):
    """
    Get all tracker details data from Supabase
    """
    response = supabase.table('tracker_details').select('*').eq('code', code).execute()
    return response


def update_tracker_details_data(code, data):
    """
    Update tracker details data from Supabase
    """
    response = supabase.table('tracker_details').update(data).eq('code', code).execute()
    return response


def insert_tracker_details_data(data):
    """
    Insert tracker details data to Supabase
    """
    response = supabase.table('tracker_details').insert(data).execute()
    return response