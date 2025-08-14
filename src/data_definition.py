"""
Data Definition Script
This script provides easy access to the stock data for TSLA, BND, and SPY.
"""

import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime

def load_stock_data():
    """
    Load stock data for TSLA, BND, and SPY
    """
    # Define our assets and time period
    tickers = ['TSLA', 'BND', 'SPY']
    start_date = '2015-07-01'
    end_date = '2025-07-31'
    
    # Download data for all tickers
    data = {}
    for ticker in tickers:
        print(f"Loading {ticker} data...")
        data[ticker] = yf.download(ticker, start=start_date, end=end_date)
        print(f"✓ {ticker}: {len(data[ticker])} trading days")
    
    return data

def clean_data(data):
    """
    Clean the data by handling missing values
    """
    cleaned_data = {}
    for ticker in data.keys():
        df = data[ticker].copy()
        
        # Forward fill any missing values (use previous day's price)
        df = df.fillna(method='ffill')
        
        # If still missing values at the beginning, use backward fill
        df = df.fillna(method='bfill')
        
        cleaned_data[ticker] = df
        print(f"✓ {ticker} data cleaned")
    
    return cleaned_data

def calculate_returns(cleaned_data):
    """
    Calculate daily returns for each asset
    """
    returns_data = {}
    for ticker in cleaned_data.keys():
        df = cleaned_data[ticker]
        close_prices = df['Close']
        daily_returns = close_prices.pct_change().dropna()
        returns_data[ticker] = daily_returns
    
    return returns_data

# Load and process the data
print("Loading stock data...")
data = load_stock_data()
cleaned_data = clean_data(data)
returns_data = calculate_returns(cleaned_data)

# Define easy access variables
df = data  # Main data dictionary with all tickers

# Individual ticker data
df_tsla = data['TSLA']
df_bnd = data['BND']
df_spy = data['SPY']

# Cleaned data
df_tsla_clean = cleaned_data['TSLA']
df_bnd_clean = cleaned_data['BND']
df_spy_clean = cleaned_data['SPY']

# Returns data
df_tsla_returns = returns_data['TSLA']
df_bnd_returns = returns_data['BND']
df_spy_returns = returns_data['SPY']

print("\n=== Data Variables Defined ===")
print("• df - main data dictionary with all tickers")
print("• df_tsla, df_bnd, df_spy - individual ticker data")
print("• df_tsla_clean, df_bnd_clean, df_spy_clean - cleaned data")
print("• df_tsla_returns, df_bnd_returns, df_spy_returns - returns data")

print(f"\nData shapes:")
print(f"TSLA: {df_tsla.shape}")
print(f"BND: {df_bnd.shape}")
print(f"SPY: {df_spy.shape}")

print("\n✓ Data successfully loaded and ready for analysis!")
