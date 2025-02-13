from prefect import task
import pandas as pd

@task
def clean_data(raw_data):
    # Basic cleaning operations
    cleaned = raw_data.dropna()
    cleaned = cleaned[cleaned['Close'] > 0]
    cleaned['Date'] = pd.to_datetime(cleaned.index)
    return cleaned