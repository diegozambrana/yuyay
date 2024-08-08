import logging
import sys

from fastapi import APIRouter, HTTPException

from ..utils.github import (
    get_repo_data,
    get_repo_stargazers_history,
    get_repo_stargazers_history_complete,
    get_organization_data,
    get_organization_stargazers_history_complete,
)
from ..utils.handlers import get_repo_format, get_organization_format
from ..utils.nixtla import forecast

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('GitHub API is starting up')

router = APIRouter(
    prefix="/api/github",
    tags=["github"],
)

@router.get("/get_repositories")
async def read_repositories(query: str):
    """
    Get repositories by owner and name
    return list of repositories success if found and fails if not found
    """
    if query is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    d = [(q.split('/')[0], q.split('/')[1]) for q in query.split(',')]
    
    fails = []
    success = []

    for owner, repo_name in d:

        if owner is None or repo_name is None:
            fails.append(f"{owner}/{repo_name}")

        repo = get_repo_data(owner, repo_name)
        logger.info(type(repo))
        
        if repo is None:
            fails.append(f"{owner}/{repo_name}")
        else:
            success.append(get_repo_format(repo))

    data = {
        'success': success,
        'fails': fails,
    }
    return data

@router.get("/get_organizations")
def read_organization(query: str):
    """
    Get organization by list of organization names
    """
    if query is None:
        raise HTTPException(status_code=404, detail="organizations not found")
    
    d = query.split(',')
    
    fails = []
    success = []

    for org in d:

        if org is None:
            fails.append(org)

        org_data = get_organization_data(org)
        
        if org_data is None:
            fails.append(f"{org_data}")
        else:
            success.append(get_organization_format(org_data))

    data = {
        'success': success,
        'fails': fails,
    }
    return data

@router.get("/org/{name}")
def read_owner_repositories(name: str):
    """
    Get repositories by owner
    """
    if name is None:
        raise HTTPException(status_code=404, detail="organization not found")

    org = get_organization_data(name)

    if org is None:
        raise HTTPException(status_code=404, detail="organization not found")

    return get_organization_format(org)

@router.get("/org/{name}/stargazers")
def read_owner_repositories(name: str):
    """
    Get repositories by owner
    """
    if name is None:
        raise HTTPException(status_code=404, detail="organization not found")

    org = get_organization_data(name)

    if org is None:
        raise HTTPException(status_code=404, detail="organization not found")
    
    data = get_organization_stargazers_history_complete(org.get('login'))

    predictions = forecast(data)

    return {
        'count': len(data),
        'data': data,
        'forecast': predictions
    }


@router.get("/{owner}/{repo_name}")
async def read_repository(owner: str, repo_name: str):
    """
    Get repository by owner and name
    """
    if owner is None or repo_name is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    repo = get_repo_data(owner, repo_name)
    if repo is None:
        raise HTTPException(status_code=404, detail="Repository not found")
    return get_repo_format(repo)


@router.get("/{owner}/{repo_name}/stargazers")
def read_stargazers(owner: str, repo_name: str):
    """
    Get stargazers by owner and name
    """
    if owner is None or repo_name is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    repo = get_repo_data(owner, repo_name)

    if repo is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    # TODO: review how to avoid the 40000 limit
    if repo['stargazers_count'] < 40000:
        data = get_repo_stargazers_history_complete(repo)
    else:
        data = get_repo_stargazers_history(owner, repo_name, repo)

    predictions = forecast(data)

    if repo is None:
        raise HTTPException(status_code=404, detail="Repository not found")

    return {
        'count': len(data),
        'data': data,
        'forecast': predictions
    }