from prefect import task
import yfinance as yf
import pandas as pd
from datetime import datetime

@task
def fetch_data():
    # Define start and end dates
    start_date = "2005-01-01"
    end_date = pd.Timestamp.today().strftime('%Y-%m-%d')

    # Ticker symbols for the top 50 companies (Nifty 50 constituents)
    nifty50 = [
        "ADANIENT.NS",    # Adani Enterprises Ltd.
        "ADANIPORTS.NS",  # Adani Ports & SEZ Ltd.
        "APOLLOHOSP.NS",  # Apollo Hospitals Enterprise Ltd.
        "ASIANPAINT.NS",  # Asian Paints Ltd.
        "AXISBANK.NS",    # Axis Bank Ltd.
        "BAJAJ-AUTO.NS",  # Bajaj Auto Ltd.
        "BAJFINANCE.NS",  # Bajaj Finance Ltd.
        "BAJAJFINSV.NS",  # Bajaj Finserv Ltd.
        "BPCL.NS",        # Bharat Petroleum Corporation Ltd.
        "BHARTIARTL.NS",  # Bharti Airtel Ltd.
        "BRITANNIA.NS",   # Britannia Industries Ltd.
        "CIPLA.NS",       # Cipla Ltd.
        "COALINDIA.NS",   # Coal India Ltd.
        "DRREDDY.NS",     # Dr. Reddy's Laboratories Ltd.
        "EICHERMOT.NS",   # Eicher Motors Ltd.
        "GRASIM.NS",      # Grasim Industries Ltd.
        "HCLTECH.NS",     # HCL Technologies Ltd.
        "HDFCBANK.NS",    # HDFC Bank Ltd.
        "HDFCLIFE.NS",    # HDFC Life Insurance Company Ltd.
        "HEROMOTOCO.NS",  # Hero MotoCorp Ltd.
        "HINDALCO.NS",    # Hindalco Industries Ltd.
        "HINDUNILVR.NS",  # Hindustan Unilever Ltd.
        "ICICIBANK.NS",   # ICICI Bank Ltd.
        "INDUSINDBK.NS",  # IndusInd Bank Ltd.
        "INFY.NS",        # Infosys Ltd.
        "ITC.NS",         # ITC Ltd.
        "JSWSTEEL.NS",    # JSW Steel Ltd.
        "KOTAKBANK.NS",   # Kotak Mahindra Bank Ltd.
        "LT.NS",          # Larsen & Toubro Ltd.
        "M&M.NS",         # Mahindra & Mahindra Ltd.
        "MARUTI.NS",      # Maruti Suzuki India Ltd.
        "NESTLEIND.NS",   # Nestlé India Ltd.
        "NTPC.NS",        # NTPC Ltd.
        "ONGC.NS",        # Oil & Natural Gas Corporation Ltd.
        "POWERGRID.NS",   # Power Grid Corporation of India Ltd.
        "RELIANCE.NS",    # Reliance Industries Ltd.
        "SBILIFE.NS",     # SBI Life Insurance Company Ltd.
        "SHRIRAMFIN.NS",  # Shriram Finance Ltd.
        "SBIN.NS",        # State Bank of India
        "SUNPHARMA.NS",   # Sun Pharmaceutical Industries Ltd.
        "TCS.NS",         # Tata Consultancy Services Ltd.
        "TATACONSUM.NS",  # Tata Consumer Products Ltd.
        "TATAMOTORS.NS",  # Tata Motors Ltd.
        "TATASTEEL.NS",   # Tata Steel Ltd.
        "TECHM.NS",       # Tech Mahindra Ltd.
        "TITAN.NS",       # Titan Company Ltd.
        "TRENT.NS",       # Trent Ltd.
        "ULTRACEMCO.NS",  # UltraTech Cement Ltd.
        "WIPRO.NS"        # Wipro Ltd.
    ]

    # Ticker symbols for the next 50 companies (Nifty Next 50 constituents)
    nifty_next_50 = [
        "ABB.NS",         # ABB India Ltd.
        "ADANIENSOL.NS",   # Adani Energy Solutions Ltd.
        "ADANIGREEN.NS",   # Adani Green Energy Ltd.
        "ADANIPOWER.NS",   # Adani Power Ltd.
        "ATGL.NS",         # Adani Total Gas Ltd.
        "AMBUJACEM.NS",    # Ambuja Cements Ltd.
        "BAJAJHLDNG.NS",   # Bajaj Holdings & Investment Ltd.
        "BANKBARODA.NS",   # Bank of Baroda
        "BHEL.NS",         # Bharat Heavy Electricals Ltd.
        "BOSCHLTD.NS",     # Bosch Ltd.
        "CANBK.NS",        # Canara Bank Ltd.
        "CHOLAFIN.NS",     # Cholamandalam Investment and Finance Co. Ltd.
        "DABUR.NS",        # Dabur India Ltd.
        "DIVISLAB.NS",     # Divi's Laboratories Ltd.
        "DLF.NS",          # DLF Ltd.
        "DMART.NS",        # DMart (Avenue Supermarts Ltd.)
        "GAIL.NS",         # GAIL (India) Ltd.
        "GODREJCP.NS",     # Godrej Consumer Products Ltd.
        "HAVELLS.NS",      # Havells India Ltd.
        "HAL.NS",          # Hindustan Aeronautics Ltd.
        "ICICIGI.NS",      # ICICI Lombard General Insurance Co. Ltd.
        "ICICIPRULI.NS",   # ICICI Prudential Life Insurance Co. Ltd.
        "IOC.NS",          # Indian Oil Corporation Ltd.
        "INDIGO.NS",       # IndiGo (InterGlobe Aviation Ltd.)
        "NAUKRI.NS",       # Info Edge (India) Ltd.
        "IRCTC.NS",        # IRCTC Ltd.
        "IRFC.NS",         # IRFC Ltd.
        "JINDALSTEL.NS",   # Jindal Steel & Power Ltd.
        "JIOFIN.NS",       # Jio Financial Services Ltd.
        "JSWENERGY.NS",    # JSW Energy Ltd.
        "LICHSGFIN.NS",    # LIC Housing Finance Ltd.
        "LTTS.NS",         # L&T Technology Services Ltd.
        "MOTHERSON.NS",    # Samvardhana Motherson International Ltd.
        "SHREECEM.NS",     # Shree Cement Ltd.
        "SIEMENS.NS",      # Siemens Ltd.
        "TATAPOWER.NS",    # Tata Power Co. Ltd.
        "TORNTPHARM.NS",   # Torrent Pharmaceuticals Ltd.
        "TVSMOTOR.NS",     # TVS Motor Company Ltd.
        "UNIONBANK.NS",    # Union Bank of India
        "UNITDSPR.NS",     # United Spirits Ltd.
        "VBL.NS",          # Varun Beverages Ltd.
        "VEDL.NS",         # Vedanta Ltd.
        "ZOMATO.NS",       # Zomato Ltd.
        "ZYDUSLIFE.NS",    # Zydus Lifesciences Ltd.
        # Additional sample candidates for the next 50:
        "IDFCFIRSTB.NS",   # IDFC First Bank Ltd.
        "YESBANK.NS",      # Yes Bank Ltd.
        "PNB.NS",          # Punjab National Bank
        "BANKINDIA.NS",    # Bank of India
        "RBLBANK.NS",      # RBL Bank Ltd.
        "INDIANB.NS"       # Indian Bank
    ]

    # Combine both lists to get a full list of 100 ticker symbols
    top_100_tickers = nifty50 + nifty_next_50

    # Data download logic
    df_list = []
    for ticker in nifty50 + nifty_next_50:
        data = yf.download(ticker, start=start_date, end=end_date)
        data['Ticker'] = ticker
        df_list.append(data)
    
    return pd.concat(df_list)