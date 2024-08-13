import json
import logging
import os
import pandas as pd
import requests
import sys

from dotenv import load_dotenv, find_dotenv

from utils.counter import get_values_list_pages
from db.mongo import (
    get_repo_data_from_db,
    insert_repo_data_to_db,
    insert_org_data_to_db,
    get_org_data_from_db,
)
from utils.handlers import (
    get_diff_stargazers_by_date,
    handle_repo_stargazers_history_complete,
    fill_missing_rows_from_list,
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('GitHub API is starting up')

_ = load_dotenv(find_dotenv())

GITHUB_TOKEN = os.environ['GITHUB_ACCESS_TOKEN']
GITHUB_API_URL = 'https://api.github.com'
GITHUB_API_HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'accept': 'application/vnd.github.v3.star+json'
}
PER_PAGE = 30


def get_organization_data(organization):
    """
    Get organization data from GitHub API
    """
    url_api = f'{GITHUB_API_URL}/orgs/{organization}'
    response_api = requests.get(url_api, headers=GITHUB_API_HEADERS)

    if response_api.status_code != 200:
        return None

    return response_api.json()


def get_repo_star_history_per_page(owner, repo_name, page):
    """
    Get repository stargazers history from GitHub API
    """
    url = f'https://api.github.com/repos/{owner}/{repo_name}/stargazers'
    params = { 'per_page': PER_PAGE, 'page': page }

    response_api = requests.get(url, params=params, headers=GITHUB_API_HEADERS)
    
    if response_api.status_code != 200:
        return None
    
    data = response_api.json()

    count = (page - 1) * PER_PAGE

    date = data[0]['starred_at']
    date = date[:10]

    return {'count': count, 'date': date}


def get_repo_data(owner, repo_name):
    """
    Get repository data from GitHub API
    """
    url_api = f'{GITHUB_API_URL}/repos/{owner}/{repo_name}'
    response_api = requests.get(url_api, headers=GITHUB_API_HEADERS)

    if response_api.status_code != 200:
        return None

    return response_api.json()

def get_repo_star_history_per_page_complete(repo, page=1, per_page=30):
    """
    Get repository stargazers history from GitHub API
    """

    owner = repo['owner']['login']
    repo_name = repo['name']

    params = {
        'per_page': per_page,
        'page': page,
    }

    url = f'https://api.github.com/repos/{owner}/{repo_name}/stargazers'

    response_api = requests.get(url, params=params, headers=GITHUB_API_HEADERS)
    
    if response_api.status_code != 200:
        return None

    return response_api.json()


def get_repo_stargazers_history(owner, repo_name, repository_data, iterations = 15):
    """
    Get repository stargazers history from GitHub API by iterations when the total stargazers is too high
    """
    total_stargazers = repository_data['stargazers_count']
    list_pages = get_values_list_pages(total_stargazers, iterations)
    result = []

    for page in list_pages:
        stars_data = get_repo_star_history_per_page(owner, repo_name, page)
        result.append(stars_data)

    return result


def get_repo_stargazers_history_complete(repository_data):
    """
    Get repository stargazers history from GitHub API complete when the total of
    stargazers is less than 40000
    """
    total_stargazers = repository_data['stargazers_count']

    data = get_repo_data_from_db(repository_data)
    logger.info(f'~~~{repository_data["full_name"]} - {total_stargazers}')

    if data:
        # if data exists in db return it
        return data['data']
    else:
        # if data does not exist in db, get it from GitHub API
        print('No data in db')
        n_pages = total_stargazers // 100 
        if total_stargazers % 100 != 0:
            n_pages += 1

        result = []
        
        # Get stargazers history for each page
        for page in range(1, n_pages + 1):
            stars_data = get_repo_star_history_per_page_complete(repository_data, page=page, per_page=100)
            result = result + [s['starred_at'] for s in stars_data]
        
        # Group by date and sum the stargazers
        result_data = handle_repo_stargazers_history_complete(result)
        result_data = json.loads(result_data)
        if  total_stargazers > 0:
            result_data = fill_missing_rows_from_list(result_data)

        # Insert data to MongoDB
        insert_repo_data_to_db(repository_data, result_data)

        return result_data


def get_repos_from_organization(org, page=1, per_page=100):
    """
    Get repositories from an organization from GitHub API
    """
    response_api = requests.get(
        f'https://api.github.com/orgs/{org}/repos?per_page={per_page}&page={page}',
        headers=GITHUB_API_HEADERS
    )
    return response_api.json()


def get_organization_stargazers_history_complete(organization_name):
    """
    Get organization stargazers history from GitHub API
    """
    
    response_org = requests.get(
        f'https://api.github.com/orgs/{organization_name}',
        headers=GITHUB_API_HEADERS
    )

    # get organization data and total of repositories
    org = response_org.json()
    total_repos = org['public_repos']

    data = get_org_data_from_db(org)

    if data:
        # if data exists in db return it
        return data['data']

    else:
        # if data does not exist in db, get it from GitHub API
        n_pages = total_repos // 100 
        
        if total_repos % 100 != 0:
            n_pages += 1
        
        total_repos = []

        # Get all repositories from the organization
        for page in range(1, n_pages + 1):
            repos = get_repos_from_organization(organization_name, page=page, per_page=100)
            total_repos = total_repos + repos

        result = []

        # Get stargazers history for each repository
        for repo in total_repos:
            repo_data = get_repo_stargazers_history_complete(repo)
            repo_data = get_diff_stargazers_by_date(repo_data)
            result = result + repo_data

        # Group by date and sum the stargazers
        df = pd.DataFrame(result)
        df = df.groupby('date').sum().reset_index()
        df = df.sort_values(by='date')
        df['total'] = df['value'].cumsum()
        df = df[['date', 'total']]
        df.columns = ['date', 'count']
        result_data = df.to_json(orient='records')
        result_data = json.loads(result_data)

        # Insert data to MongoDB
        insert_org_data_to_db(org, result_data)

        return result_data