import json
import pypistats
import pandas as pd
from utils.nixtla import forecast
from db.python_packages_data import (
    get_pystats_data_from_db,
    insert_pystats_data_to_db,
)

import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info('PyStats API is starting up')


def get_downloads_data(package_name):
    """
    Get the downloads data from pypi
    """
    response = get_pystats_data_from_db(package_name)

    if len(response.data) > 0:
        # if data exists in db return it
        return response.data[0]
    else:
        try:
            data =  pypistats.overall(
                package_name,
                mirrors=False,
                total=True,
                format="json"
            )

            data = json.loads(data)
            result = [{'date': d['date'], 'count': d['downloads']} for d in data['data']]
            df_result = pd.DataFrame(result)
            prediction = forecast(df_result)
            insert_pystats_data_to_db(package_name, result, prediction)

            return {
                'data': result,
                'prediction': prediction,
            }
        except Exception as e:
                return None
