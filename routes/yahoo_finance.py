import logging
import sys
import csv
import codecs

from fastapi import APIRouter, HTTPException, File, UploadFile
from ..utils.handlers import load_csv_to_pandas

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')

router = APIRouter(
    prefix="/api/yahoo_finance",
    tags=["yahoo finance reader"],
)

@router.post("/load_csv")
async def load_csv_yahoo_finance(file: UploadFile = File(...)):
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    df_csv = load_csv_to_pandas(csvReader)
    logger.info(f"df_csv: {df_csv.head()}")
    return {"message": "CSV loaded successfully"}