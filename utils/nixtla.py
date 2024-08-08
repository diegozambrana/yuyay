# Accurate forecasting with TimeGPT

import os
import json
import logging
import sys
import pandas as pd

from nixtla import NixtlaClient
from dotenv import load_dotenv, find_dotenv

from .handlers import fill_missing_rows

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('Nixtla API is starting up')

_ = load_dotenv(find_dotenv())

NIXTLA_API_KEY = os.environ['NIXTLA_API_KEY']

nixtla_client = NixtlaClient(api_key=NIXTLA_API_KEY)

def forecast(data, time_col="date", val_col="count", horizon=30):
    """
    Forecast data with TimeGPT
    get a list of dictionaries {date: value, count: value}
    return the forecast data as a list of dictionaries {date: value, count: value}
    """
    logger.info('forecast')
    logger.info(data[0])
    df = pd.DataFrame(data)
    df = fill_missing_rows(df)
    forecast_df = nixtla_client.forecast(df=df, h=horizon, time_col=time_col, target_col=val_col)
    forecast_df.columns = ['date', 'count']
    forecast_data = json.loads(forecast_df.to_json(orient='records'))
    return forecast_data