import csv
import json
import pandas as pd

def get_repo_format(response):
    return {
        'full_name': response['full_name'],
        'name': response['name'],
        'owner': response['owner']['login'],
        "avatar_url": response['owner']['avatar_url'],
        'description': response['description'],
        'stargazers_count': response['stargazers_count'],
        'html_url': response['html_url'],
        'language': response['language'],
    }

def get_organization_format(response):
    return {
        'login': response['login'],
        'name': response['name'],
        'avatar_url': response['avatar_url'],
        'html_url': response['html_url'],
        'description': response['description'],
        'created_at': response['created_at'],
        'public_repos': response['public_repos'],
    }

def handle_repo_stargazers_history_complete(dates_list):
    """
    get the accumulated stargazers by date based in the list stored in DB
    """
    df_dates_list = pd.DataFrame(dates_list, columns=['starred_at'])
    df_dates_list['starred_at'] = df_dates_list['starred_at'].apply(lambda x: x[:10])
    df_dates_list = df_dates_list.groupby('starred_at').size().reset_index(name='counts')
    df_dates_list['total'] = df_dates_list['counts'].cumsum()
    df_result = df_dates_list[['starred_at', 'total']]
    df_result.columns = ['date', 'count']
    return df_result.to_json(orient='records')


def get_diff_stargazers_by_date(list_dates):
    """
    get the list of stargazers by date based in the list stored in DB
    """
    df_dates_list = pd.DataFrame(list_dates, columns=['date', 'count'])
    df_dates_list['day_count'] = df_dates_list['count'].diff().fillna(0)
    date_list = json.loads(df_dates_list.to_json(orient='records'))
    if len(date_list) > 0:
        date_list[0]['day_count'] = date_list[0]['count']
        date_list = [{'date': d['date'], 'value': int(d['day_count'])} for d in date_list]
        return date_list
    else:
        return []


def fill_missing_rows(df_original):
    """
    fill the missing rows in the dataframe
    some days are missing in the data, so the value are filled with the last value
    """
    df = df_original.copy()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df = df.resample('D').ffill()
    df = df.reset_index()
    return df

def fill_missing_rows_from_list(list_original):
    """
    fill the missing rows in the list
    some days are missing in the data, so the value are filled with the last value
    """
    df = fill_missing_rows(pd.DataFrame(list_original, columns=['date', 'count']))
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    result = df.to_json(orient='records')
    return json.loads(result)

# TODO: review if this function is necessary
def load_csv_to_pandas(csvReader: csv.DictReader) -> pd.DataFrame:
    return pd.DataFrame(csvReader)

