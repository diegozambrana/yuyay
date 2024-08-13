import logging
import sys

import yfinance as yf

from db.yahoo_finance_data import get_by_symbol
from datetime import datetime
from utils.nixtla import forecast
from db.yahoo_finance_data import insert_yahoo_finance, update_yahoo_finance

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('GitHub API is starting up')

def get_yahoo_finance(symbol: str = 'BTC-USD', start_date: str = '2023-01-01', end_date: str = datetime.now().strftime("%Y-%m-%d")):
    data = yf.download(symbol, start=start_date, end=end_date)
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
    prediction = forecast(data, time_col="Date", val_col="Close", horizon=7)

    return {
        'count': len(data),
        'data': data.to_dict(orient='records'),
        'forecast': prediction
    }


def get_or_create_yahoo_finance(symbol: str, start_date: str = '2023-01-01', end_date: str = datetime.now().strftime("%Y-%m-%d")):
    """
    Get the Yahoo Finance data from the database or create it if it does not exist.
    """
    response = get_by_symbol(symbol)

    if len(response.data) == 0:
        data = get_yahoo_finance(symbol, start_date, end_date)

        # insert the data into the database
        insert_yahoo_finance({
            'symbol': symbol,
            'name': symbol,
            'data': data['data'],
            'prediction': data['forecast']
        })
        return data
    else:
        if not response.data[0]['updated_at'].startswith(end_date):
            data = get_yahoo_finance(symbol, start_date, end_date)

            # update the data in the database
            update_yahoo_finance(symbol, {
                'data': data['data'],
                'prediction': data['forecast']
            })
            return data
        else:
            return {
                'count': len(response.data[0]['data']),
                'data': response.data[0]['data'],
                'forecast': response.data[0]['prediction']
            }