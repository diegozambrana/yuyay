import csv
import pandas as pd


def load_csv_to_pandas(csvReader: csv.DictReader) -> pd.DataFrame:
    return pd.DataFrame(csvReader)

