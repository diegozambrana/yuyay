import logging
import sys

from datetime import datetime
from db.supabase import supabase

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')


def insert_repo_data_to_db(repo, data, forecast):
    """
    Insert repository data to Supabase and stargazers data history
    """
    response = supabase.table('github_repository_star').insert({
        'owner': repo['owner']['login'],
        'full_name': repo['full_name'],
        'stargazers_count': repo['stargazers_count'],
        'data': data,
        'prediction': forecast
    }).execute()
    return response


def get_repo_data_from_db(repo):
    """
    Get repository data from Supabase
    """
    response = supabase.table('github_repository_star').select('*').eq('full_name', repo['full_name']).execute()
    return response


def update_repo_data_to_db(repo, data, forecast):
    """
    Update repository data to Supabase
    """
    response = supabase.table('github_repository_star').update({
        'stargazers_count': repo['stargazers_count'],
        'updated_at': datetime.now().isoformat(),
        'data': data,
        'prediction': forecast
    }).eq('full_name', repo['full_name']).execute()
    return response


def insert_org_data_to_db(org, data, forecast):
    """
    Insert organization data to Supabase and stargazers data history
    """
    response = supabase.table('github_organization_star').insert({
        'name': org['login'],
        'data': data,
        'prediction': forecast
    }).execute()
    return response


def get_org_data_from_db(org):
    """
    Get organization data from Supabase
    """
    response = supabase.table('github_organization_star').select('*').eq('name', org['login']).execute()
    return response


def update_org_data_to_db(org, data, forecast):
    """
    Update organization data to Supabase
    """
    response = supabase.table('github_organization_star').update({
        'updated_at': datetime.now().isoformat(),
        'data': data,
        'prediction': forecast
    }).eq('name', org['login']).execute()
    return response


def get_pystats_data_from_db(name):
    """
    Get PyStats data from Supabase
    """
    response = supabase.table('package_python_downloads').select('*').eq('name', name).execute()
    return response


def insert_pystats_data_to_db(name, data, forecast):
    """
    Insert PyStats data to Supabase
    """
    response = supabase.table('package_python_downloads').insert({
        'name': name,
        'data': data,
        'prediction': forecast
    }).execute()
    return response


def update_pystats_data_to_db(name, data, forecast):
    """
    Update PyStats data to Supabase
    """
    response = supabase.table('package_python_downloads').update({
        'updated_at': datetime.now().isoformat(),
        'data': data,
        'prediction': forecast
    }).eq('name', name).execute()
    return response