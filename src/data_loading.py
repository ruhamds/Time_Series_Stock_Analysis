"""
This script fetches historical financial data for TSLA, BND, and SPY using yfinance
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for a given ticker
    
    Args:
        ticker (str): Stock ticker symbol
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
        pd.DataFrame: Historical stock data
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(start=start_date, end=end_date)
        
        if data.empty:
            print(f"Warning: No data found for {ticker}")
            return None
            
        # Add ticker column for identification
        data['Ticker'] = ticker
        print(f"Successfully fetched data for {ticker}: {len(data)} records")
        return data
        
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None

def load_all_assets():
    """
    Load data for all three assets: TSLA, BND, SPY
    
    Returns:
        dict: Dictionary containing dataframes for each asset
    """
    # Define our assets
    tickers = ['TSLA', 'BND', 'SPY']
    start_date = '2015-07-01'
    end_date = '2025-07-31'
    
    print("Starting data fetch...")
    print(f"Period: {start_date} to {end_date}")
    print("-" * 40)
    
    asset_data = {}
    
    for ticker in tickers:
        print(f"Fetching data for {ticker}...")
        data = fetch_stock_data(ticker, start_date, end_date)
        
        if data is not None:
            asset_data[ticker] = data
        else:
            print(f"Failed to fetch data for {ticker}")
    
    print("-" * 40)
    print(f"Data loading complete. Loaded {len(asset_data)} assets.")
    
    return asset_data

def basic_data_info(asset_data):
    """
    Display basic information about loaded data
    
    Args:
        asset_data (dict): Dictionary containing asset dataframes
    """
    print("\n=== DATA OVERVIEW ===")
    
    for ticker, data in asset_data.items():
        print(f"\n{ticker}:")
        print(f"  Date range: {data.index.min().date()} to {data.index.max().date()}")
        print(f"  Total records: {len(data)}")
        print(f"  Columns: {list(data.columns)}")
        print(f"  Missing values: {data.isnull().sum().sum()}")

def save_data(asset_data, folder='data'):
    """
    Save the loaded data to CSV files
    
    Args:
        asset_data (dict): Dictionary containing asset dataframes
        folder (str): Folder to save data files
    """
    import os
    
    if not os.path.exists(folder):
        os.makedirs(folder)
    
    for ticker, data in asset_data.items():
        filename = f"{folder}/{ticker}_data.csv"
        data.to_csv(filename)
        print(f"Saved {ticker} data to {filename}")

if __name__ == "__main__":
    # Load all asset data
    assets = load_all_assets()
    
    # Display basic information
    if assets:
        basic_data_info(assets)
        
        # Save data to files
        save_data(assets)
        
        print("\nData loading completed successfully!")
    else:
        print("Failed to load any asset data.")