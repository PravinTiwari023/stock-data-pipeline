from prefect import task
from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

@task
def get_data():
    # Get today's date
    today = datetime.today()

    # Calculate the first and last day of the previous month
    first_day_last_month = today.replace(day=1) - timedelta(days=1)
    first_day_last_month = first_day_last_month.replace(day=1)
    last_day_last_month = first_day_last_month.replace(day=28) + timedelta(days=4)
    last_day_last_month = last_day_last_month - timedelta(days=last_day_last_month.day)

    start_date = first_day_last_month.strftime('%Y-%m-%d')
    end_date = last_day_last_month.strftime('%Y-%m-%d')

    # List of stock tickers for India's top 50 companies
    tickers = [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "BAJFINANCE.NS",
        "KOTAKBANK.NS", "HCLTECH.NS", "ASIANPAINT.NS", "LT.NS", "AXISBANK.NS",
        "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS",
        "NESTLEIND.NS", "M&M.NS", "TECHM.NS", "POWERGRID.NS", "TATAMOTORS.NS",
        "INDUSINDBK.NS", "SBILIFE.NS", "DIVISLAB.NS", "BAJAJFINSV.NS", "ADANIPORTS.NS",
        "HDFCLIFE.NS", "GRASIM.NS", "ONGC.NS", "COALINDIA.NS", "JSWSTEEL.NS",
        "DRREDDY.NS", "BRITANNIA.NS", "CIPLA.NS", "SHREECEM.NS", "HEROMOTOCO.NS",
        "BPCL.NS", "EICHERMOT.NS", "TATACONSUM.NS", "ADANIENT.NS",
        "HINDALCO.NS", "IOC.NS", "BAJAJ-AUTO.NS", "APOLLOHOSP.NS", "TATASTEEL.NS"
    ]

    # Download data for each ticker
    stock_data = {}
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        stock_data[ticker] = df

    # Create list of tuples with ticker and dataframe
    dataframes = [(stock_data[ticker], ticker) for ticker in [
        "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
        "HINDUNILVR.NS", "ITC.NS", "SBIN.NS", "BHARTIARTL.NS", "BAJFINANCE.NS",
        "KOTAKBANK.NS", "HCLTECH.NS", "ASIANPAINT.NS", "LT.NS", "AXISBANK.NS",
        "MARUTI.NS", "SUNPHARMA.NS", "TITAN.NS", "ULTRACEMCO.NS", "WIPRO.NS",
        "NESTLEIND.NS", "M&M.NS", "TECHM.NS", "POWERGRID.NS", "TATAMOTORS.NS",
        "INDUSINDBK.NS", "SBILIFE.NS", "DIVISLAB.NS", "BAJAJFINSV.NS", "ADANIPORTS.NS",
        "HDFCLIFE.NS", "GRASIM.NS", "ONGC.NS", "COALINDIA.NS", "JSWSTEEL.NS",
        "DRREDDY.NS", "BRITANNIA.NS", "CIPLA.NS", "SHREECEM.NS", "HEROMOTOCO.NS",
        "BPCL.NS", "EICHERMOT.NS", "TATACONSUM.NS", "ADANIENT.NS",
        "HINDALCO.NS", "IOC.NS", "BAJAJ-AUTO.NS", "APOLLOHOSP.NS", "TATASTEEL.NS"
    ]]
    
    # Process each dataframe
    processed_dfs = []
    for df, ticker in dataframes:
        # Rename columns
        df.columns = ['Close', 'High', 'Low', 'Open', 'Volume']
        
        # Reset index
        df = df.reset_index()
        
        # Add stock ticker column
        df['Stock_Ticker'] = ticker
        
        processed_dfs.append(df)
    
    # Concatenate all dataframes into a single dataframe
    combined_df = pd.concat(processed_dfs, ignore_index=True)

    return combined_df