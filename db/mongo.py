import os
from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient
from datetime import datetime
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('GitHub API is starting up')

_ = load_dotenv(find_dotenv())

MONGODB_ACCESS_URL = os.environ['MONGODB_ACCESS_URL']


def insert_repo_data_to_db(repo, data):
    """
    Insert repository data to MongoDB and stargazers data history
    """
    client = MongoClient(MONGODB_ACCESS_URL)
    db = client.trackerDB
    collection = db.repositoriesStargazersDataHistory
    collection.insert_one({
        'owner': repo['owner']['login'],
        'full_name': repo['full_name'],
        'stargazers_count': repo['stargazers_count'],
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'data': data
    })


def get_repo_data_from_db(repo):
    """
    Get repository data from MongoDB
    """
    client = MongoClient(MONGODB_ACCESS_URL)
    db = client.trackerDB
    collection = db.repositoriesStargazersDataHistory
    data = collection.find_one({'full_name': repo['full_name']})
    client.close()
    return data


def update_repo_data_to_db(repo, data):
    """
    Update repository data to MongoDB
    """
    client = MongoClient(MONGODB_ACCESS_URL)
    db = client.trackerDB
    collection = db.repositoriesStargazersDataHistory
    
    collection.update_one({
        'full_name': repo['full_name']
    }, {
        '$set': {
            'stargazers_count': repo['stargazers_count'],
            'updated_at': datetime.now().isoformat(),
            'data': data
        }
    })
    repo_data = collection.find_one({'full_name': repo['full_name']})
    client.close()

    return repo_data


def insert_org_data_to_db(org, data):
    """
    Insert organization data to MongoDB and stargazers data history
    """
    client = MongoClient(MONGODB_ACCESS_URL)
    db = client.trackerDB
    collection = db.organizationStargazersDataHistory
    collection.insert_one({
        'name': org['login'],
        'public_repos': org['public_repos'],
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'data': data
    })
    client.close()


def get_org_data_from_db(org):
    """
    Get organization data from MongoDB
    """
    client = MongoClient(MONGODB_ACCESS_URL)
    db = client.trackerDB
    collection = db.organizationStargazersDataHistory
    data = collection.find_one({'name': org['login']})
    client.close()
    return data


def get_pystats_data_from_db(package_name):
    """
    Get python package data from MongoDB
    """
    client = MongoClient(MONGODB_ACCESS_URL)
    db = client.trackerDB
    collection = db.pythonPackagesDataHistory
    data = collection.find_one({'package_name': package_name})
    client.close()
    return data


def insert_pystats_data_to_db(package_name, data):
    """
    Insert python package data to MongoDB
    """
    client = MongoClient(MONGODB_ACCESS_URL)
    db = client.trackerDB
    collection = db.pythonPackagesDataHistory
    collection.insert_one({
        'package_name': package_name,
        'created_at': datetime.now().isoformat(),
        'updated_at': datetime.now().isoformat(),
        'data': data
    })
    client.close()