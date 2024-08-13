import json
import pypistats
from db.mongo import get_pystats_data_from_db, insert_pystats_data_to_db


def get_downloads_data(package_name):
    """
    Get the downloads data from pypi
    """
    data = get_pystats_data_from_db(package_name)

    if data:
        return data['data']
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

            insert_pystats_data_to_db(package_name, result)

            return result
        except Exception as e:
                return None


