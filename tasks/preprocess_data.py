import pandas as pd
import numpy as np

def preprocess_data(df):
    """
    Preprocess the DataFrame to fix the issues found in data validation:
    
    1. Ensure 'Close', 'High', 'Low', 'Open' are non-negative.
    2. Handle the 'Stock_Ticker' uniqueness issue by ensuring each row has a unique identifier.

    :param df: pandas DataFrame with columns 'Date', 'Close', 'High', 'Low', 'Open', 'Volume', 'Stock_Ticker'
    :return: Preprocessed DataFrame
    """

    # 1. Convert negative values in price-related columns to their absolute values
    # This assumes negative values are errors and we want their magnitude, which might not always be the case
    price_columns = ['Close', 'High', 'Low', 'Open']
    for column in price_columns:
        df[column] = df[column].abs()  # Using abs() to convert negative numbers to positive

    # 2. Handle 'Stock_Ticker' uniqueness:
    # If 'Stock_Ticker' should be unique for each row but isn't, you might want to:
    # - Add a unique identifier to the ticker if this dataset represents multiple stocks over time
    # Here, I'm assuming we want to keep the ticker but add a sequential number for uniqueness:
    df['Stock_Ticker'] = df.groupby('Stock_Ticker').cumcount().add(1).astype(str).str.zfill(5) + '_' + df['Stock_Ticker']

    # If you want to ensure 'Stock_Ticker' is always the same but unique per entry, you might do:
    # df['Stock_Ticker'] = df.index.map(lambda x: f"{x}_{df['Stock_Ticker'].iloc[0]}")

    # Additional steps you might want to consider:
    # - Check and convert 'Date' to datetime if not already done
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert to datetime, coercing invalid dates to NaT

    # - Handle any NaN or infinite values if they exist
    df.replace([np.inf, -np.inf], np.nan, inplace=True)  # Replace infinite values with NaN
    df.dropna(inplace=True)  # Drop rows with NaN values, or you could fill them if that's more appropriate

    return df