import logging
import sys
from datetime import datetime, timezone


from fastapi import APIRouter, HTTPException
from db.tracker_data import (
    insert_tracker_data,
    get_tracker_data,
    delete_tracker_data,
    update_tracker_data,
    get_tracker_details_by_code,
    get_tracker_details_data,
    insert_tracker_details_data,
    update_tracker_details_data,
    get_tracking_list_by_tracker_details_id
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')

router = APIRouter(
    prefix="/api/tracker",
    tags=["Tracker API"],
)

# TRACKER DETAILS

@router.get("/trackers")
async def get_tracker_details():
    """
    Get all tracker details
    """
    try:
        response = get_tracker_details_data()
        return response.data
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")


@router.get("/trackers/{code}")
async def fetch_tracker_details_by_code(code: str):
    """
    Get all tracker details by code
    """
    try:
        response = get_tracker_details_by_code(code)
        return response.data[0]
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")
    

@router.get("/trackers/{tracker_details_id}/tracks")
async def fetch_tracker_details_by_tracker_details_id(tracker_details_id: str):
    """
    Get all tracker details by tracker_details_id
    """
    try:
        response = get_tracking_list_by_tracker_details_id(tracker_details_id)
        return response.data
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")


@router.post("/trackers")
async def create_tracker_details(data: dict):
    """
    Get all tracker details
    payload:
    {
        "name": "test",
        "description": "",
        "details": [{"type": "string", "field": "test_1", "label": "Test 1"}, ...]
    }
    """
    try:
        data['code'] = data['name'].lower().replace(" ", "-")
        response = insert_tracker_details_data(data)
        return response.data
    except Exception as e:
        return HTTPException(status_code=401, detail="Issue creating tracker details")


@router.put("/trackers/{code}")
async def update_tracker_details(code: str, data: dict):
    """
    update tracker details
    payload:
    {
        "description": "",
        "details": [{"type": "string", "field": "test_1", "label": "Test 1"}, ...]
    }
    """
    try:
        response = update_tracker_details_data(code, data)
        return response.data
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")



# TRACKER

@router.post("/start_track/{tracker_details_id}")
async def start_tracking(tracker_details_id: str):
    """
    create a new track with based in tracker details
    """
    try:
        logger.info(f"start_tracking: {tracker_details_id}")
        response = insert_tracker_data({
            "tracker_details_id": tracker_details_id,
            "status": "started",
        })
        logger.info(response.data[0]['tracker_id'])
        return {
            "message": "Tracking started",
            "tracker_id": response.data[0]['tracker_id']
        }
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")


@router.put("/{tracking_id}")
async def update_tracking(tracking_id: str, data: dict):
    """
    update tracking data based in details from tracker_details table
    """
    try:
        logger.info(f"update_tracking: {tracking_id}")
        update_tracker_data(tracking_id, {"data": data})
        return {"message": "Tracking updated"}
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")


@router.put("/{tracking_id}/finish_track")
async def finish_tracking(tracking_id: str):
    """
    finish tracker by tracking_id
    """
    try:
        logger.info(f"finish_tracking: {tracking_id}")
        data = {
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "status": "finished",
        }
        update_tracker_data(tracking_id, data)
        return {"message": "Tracking finished"}
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")


@router.get("/{tracking_id}")
async def get_tracking(tracking_id: str):
    """
    get details of the tracker by tracking_id
    """
    try:
        logger.info(f"get_tracking: {tracking_id}")
        response = get_tracker_data(tracking_id)
        return response.data
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")

@router.delete("/{tracking_id}")
async def delete_tracking(tracking_id: str):
    """
    DELETE tracker by tracking_id
    """
    try:
        logger.info(f"delete_tracking: {tracking_id}")
        delete_tracker_data(tracking_id)
        return {"message": "Tracking delete"}
    except Exception as e:
        return HTTPException(status_code=404, detail="Tracker details not found")
