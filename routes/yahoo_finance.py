import logging
import sys
import csv
import codecs

from fastapi import APIRouter, HTTPException, File, UploadFile
from utils.handlers import load_csv_to_pandas
from utils.nixtla import forecast
import yfinance as yf
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')

router = APIRouter(
    prefix="/api/yahoo_finance",
    tags=["yahoo finance reader"],
)

@router.get("/")
async def get_yahoo_finance(symbol: str = 'BTC-USD'):
    """
    Get the historical data from Yahoo Finance and return the data with the forecast.
    """
    try:
        current_date = datetime.now().strftime("%Y-%m-%d")
        data = yf.download(symbol, start='2020-01-01', end=current_date)
        data.reset_index(inplace=True)
        prediction = forecast(data, time_col="Date", val_col="Close", horizon=7)
        return {
            'count': len(data),
            'data': data[['Date', 'Close']].to_dict(orient='records'),
            'forecast': prediction
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting data from Yahoo Finance")


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