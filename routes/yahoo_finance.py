import logging
import sys
import csv
import codecs

from fastapi import APIRouter, HTTPException, File, UploadFile
from utils.handlers import load_csv_to_pandas
from utils.nixtla import forecast

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
    """
    Load a CSV file from Yahoo Finance and return the data with the forecast.
    """
    csv_reader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'))
    df_csv = load_csv_to_pandas(csv_reader)
    df_csv['Close'] = df_csv['Close'].astype(float)
    prediction = forecast(df_csv, time_col="Date", val_col="Close", horizon=7)
    return {
        'count': len(df_csv),
        'data': df_csv[['Date', 'Close']].to_dict(orient='records'),
        'forecast': prediction
    }