from prefect import task
import pandas as pd
import numpy as np

@task
def clean_data(df):
    """
    Clean the processed data for further analysis or storage.

    :param df: DataFrame after preprocessing
    :return: Cleaned DataFrame
    """
    
    # Handle missing data
    df.dropna(inplace=True)

    # Ensure data consistency
    df = df[df['High'] >= df['Low']]  # Logical check for stock prices
    df = df[df['Volume'] > 0]  # Ensure volume is positive

    # Unique identifiers
    df.drop_duplicates(subset=['Date', 'Stock_Ticker'], keep='first', inplace=True)

    # Correct data types
    df['Date'] = pd.to_datetime(df['Date'])
    
    return df