import logging
import sys

from fastapi import APIRouter, HTTPException

from utils.nixtla import forecast
from core.pystats import get_downloads_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')

router = APIRouter(
    prefix="/api/py",
    tags=["python packages"],
)


@router.get("/packages")
async def get_package_data(query: str | None = None):
    """
    Get the data of a python package from pypi
    """
    if query is None:
        raise HTTPException(status_code=404, detail="organizations not found")
    
    d = query.split(',')

    fails = []
    success = []

    for package_name in d:

        data = get_downloads_data(package_name)

        if data is None:
            fails.append(package_name)
        else:
            prediction = forecast(data)

            success.append({
                'name': package_name,
                'data': data,
                'forecast': prediction,
            })

    data = {
        'success': success,
        'fails': fails,
    }

    return data


@router.get("/{package_name}")
async def get_package_data(package_name: str):
    """
    Get the data of a python package from pypi
    """
    if package_name is None:
        raise HTTPException(status_code=404, detail="Package not found")

    data = get_downloads_data(package_name)

    if data is None:
        raise HTTPException(status_code=404, detail="Package not found")

    prediction = forecast(data)

    return {
        'name': package_name,
        'data': data,
        'forecast': prediction,
    }