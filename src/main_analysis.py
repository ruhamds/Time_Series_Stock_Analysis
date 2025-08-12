"""
Main analysis script for Portfolio Management Task 1
This script orchestrates the complete analysis workflow
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Import our custom modules
from config import DATA_CONFIG, ASSET_INFO, ANALYSIS_CONFIG
from utils import *
from data_loading import load_all_assets, save_data

def main():
    """
    Main function to run the complete Task 1 analysis
    """
    print("="*60)
    print("PORTFOLIO MANAGEMENT ANALYSIS - TASK 1")
    print("Time Series Forecasting for Portfolio Optimization")
    print("="*60)
    
    # Step 1: Load Data
    print("\n1. DATA LOADING")
    print("-" * 30)
    
    # Check if data already exists
    if os.path.exists('data/TSLA_data.csv'):
        print("Loading existing data...")
        tsla = pd.read_csv('data/TSLA_data.csv', index_col=0, parse_dates=True)
        bnd = pd.read_csv('data/BND_data.csv', index_col=0, parse_dates=True)
        spy = pd.read_csv('data/SPY_data.csv', index_col=0, parse_dates=True)
        assets = {'TSLA': tsla, 'BND': bnd, 'SPY': spy}
    else:
        print("Fetching fresh data...")
        assets = load_all_assets()
        if assets:
            save_data(assets)
    
    if not assets:
        print("Failed to load data. Exiting...")
        return
    
    # Step 2: Data Cleaning and Preprocessing
    print("\n2. DATA CLEANING AND PREPROCESSING")
    print("-" * 40)
    
    for ticker, data in assets.items():
        # Handle missing values
        missing_before = data.isnull().sum().sum()
        assets[ticker] = data.fillna(method='ffill').fillna(method='bfill')
        missing_after = assets[ticker].isnull().sum().sum()
        
        # Calculate additional features
        assets[ticker]['Daily_Return'] = calculate_returns(data['Close'])
        assets[ticker]['Volatility_20'] = calculate_rolling_volatility(
            assets[ticker]['Daily_Return'], ANALYSIS_CONFIG['rolling_window']
        )
        assets[ticker]['MA_20'] = data['Close'].rolling(ANALYSIS_CONFIG['rolling_window']).mean()
        
        print(f"{ticker}: Missing values {missing_before} → {missing_after}")
    
    # Step 3: Exploratory Data Analysis
    print("\n3. EXPLORATORY DATA ANALYSIS")
    print("-" * 35)
    
    # Basic statistics
    print("\nBasic Statistics:")
    for ticker, data in assets.items():
        returns = data['Daily_Return'].dropna()
        print(f"\n{ticker} ({ASSET_INFO[ticker]['description']}):")
        print(f"  Period: {data.index.min().date()} to {data.index.max().date()}")
        print(f"  Total records: {len(data)}")
        print(f"  Average daily return: {returns.mean()*100:.3f}%")
        print(f"  Daily volatility: {returns.std()*100:.3f}%")
        print(f"  Min return: {returns.min()*100:.2f}%")
        print(f"  Max return: {returns.max()*100:.2f}%")
    
    # Step 4: Stationarity Analysis
    print("\n4. STATIONARITY ANALYSIS")
    print("-" * 30)
    
    stationarity_results = {}
    for ticker, data in assets.items():
        print(f"\n{ticker} Stationarity Tests:")
        
        # Test prices
        price_test = perform_adf_test(data['Close'], f"{ticker} Prices")
        print(f"  Prices: {'Stationary' if price_test['is_stationary'] else 'Non-Stationary'}")
        print(f"    ADF Statistic: {price_test['adf_statistic']:.4f}")
        print(f"    P-value: {price_test['p_value']:.6f}")
        
        # Test returns
        returns_test = perform_adf_test(data['Daily_Return'].dropna(), f"{ticker} Returns")
        print(f"  Returns: {'Stationary' if returns_test['is_stationary'] else 'Non-Stationary'}")
        print(f"    ADF Statistic: {returns_test['adf_statistic']:.4f}")
        print(f"    P-value: {returns_test['p_value']:.6f}")
        
        stationarity_results[ticker] = {
            'prices': price_test,
            'returns': returns_test
        }
    
    # Step 5: Risk Metrics Calculation
    print("\n5. RISK METRICS CALCULATION")
    print("-" * 35)
    
    risk_metrics = {}
    for ticker, data in assets.items():
        returns = data['Daily_Return'].dropna()
        
        metrics = {
            'annual_return': annualize_metrics(returns.mean(), 'return'),
            'annual_volatility': annualize_metrics(returns.std(), 'volatility'),
            'sharpe_ratio': annualize_metrics(calculate_sharpe_ratio(returns), 'sharpe'),
            'var_5': calculate_var(returns, 0.05),
            'var_1': calculate_var(returns, 0.01),
            'cvar_5': calculate_cvar(returns, 0.05),
            'max_drawdown': calculate_max_drawdown(data['Close'])
        }
        
        risk_metrics[ticker] = metrics
        
        print(f"\n{ticker} Risk Metrics:")
        print(f"  Annual Return: {metrics['annual_return']*100:.2f}%")
        print(f"  Annual Volatility: {metrics['annual_volatility']*100:.2f}%")
        print(f"  Sharpe Ratio: {metrics['sharpe_ratio']:.3f}")
        print(f"  Daily VaR (5%): {metrics['var_5']*100:.2f}%")
        print(f"  Daily CVaR (5%): {metrics['cvar_5']*100:.2f}%")
        print(f"  Max Drawdown: {metrics['max_drawdown']*100:.2f}%")
    
    # Step 6: Outlier Detection
    print("\n6. OUTLIER ANALYSIS")
    print("-" * 25)
    
    for ticker, data in assets.items():
        returns = data['Daily_Return'].dropna()
        outliers = detect_outliers(returns, threshold=3)
        
        print(f"\n{ticker} Outliers (>3σ):")
        print(f"  Total outliers: {len(outliers)}")
        
        if len(outliers) > 0:
            print("  Top 3 extreme movements:")
            top_outliers = outliers.abs().nlargest(3)
            for date, return_val in top_outliers.items():
                direction = "↑" if outliers[date] > 0 else "↓"
                print(f"    {date.date()}: {direction} {abs(outliers[date])*100:.2f}%")
    
    # Step 7: Correlation Analysis
    print("\n7. CORRELATION ANALYSIS")
    print("-" * 30)
    
    # Create returns dataframe
    returns_df = pd.DataFrame({
        ticker: data['Daily_Return'] for ticker, data in assets.items()
    }).dropna()
    
    correlation_matrix = returns_df.corr()
    print("\nCorrelation Matrix:")
    print(correlation_matrix.round(3))
    
    # Step 8: Generate Summary Report
    print("\n8. COMPREHENSIVE SUMMARY")
    print("-" * 30)
    
    summary_table = create_summary_table(assets)
    print("\nComplete Risk-Return Profile:")
    print(summary_table)
    
    # Step 9: Investment Insights
    print("\n9. INVESTMENT INSIGHTS")
    print("-" * 30)
    
    print("\nAsset Characteristics:")
    print(f"• TSLA: {ASSET_INFO['TSLA']['description']}")
    print(f"  - Highest return potential: {risk_metrics['TSLA']['annual_return']*100:.1f}% annual")
    print(f"  - Highest volatility: {risk_metrics['TSLA']['annual_volatility']*100:.1f}% annual")
    print(f"  - Moderate risk-adjusted return: {risk_metrics['TSLA']['sharpe_ratio']:.2f} Sharpe")
    
    print(f"\n• BND: {ASSET_INFO['BND']['description']}")
    print(f"  - Stable returns: {risk_metrics['BND']['annual_return']*100:.1f}% annual")
    print(f"  - Lowest risk: {risk_metrics['BND']['annual_volatility']*100:.1f}% volatility")
    print(f"  - Good for diversification")
    
    print(f"\n• SPY: {ASSET_INFO['SPY']['description']}")
    print(f"  - Market-level returns: {risk_metrics['SPY']['annual_return']*100:.1f}% annual")
    print(f"  - Moderate risk: {risk_metrics['SPY']['annual_volatility']*100:.1f}% volatility")
    print(f"  - Solid risk-adjusted return: {risk_metrics['SPY']['sharpe_ratio']:.2f} Sharpe")
    
    print("\nPortfolio Construction Implications:")
    print("• TSLA can boost portfolio returns but increases overall risk")
    print("• BND provides stability and helps reduce portfolio volatility")  
    print("• SPY offers broad market exposure with balanced risk-return")
    print("• Combining all three allows for risk-return optimization")
    
    # Step 10: Save Results
    print("\n10. SAVING RESULTS")
    print("-" * 25)
    
    # Save summary table
    save_results(summary_table, 'task1_summary_results.csv')
    
    # Save correlation matrix
    correlation_matrix.to_csv('correlation_matrix.csv')
    print("Correlation matrix saved to correlation_matrix.csv")
    
    print("\n" + "="*60)
    print("TASK 1 ANALYSIS COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("\nNext Steps:")
    print("• Review the generated summary files")
    print("• Run EDA.ipynb for detailed visualizations")
    print("• Run metrics.ipynb for advanced risk analysis")
    print("• Proceed to Task 2 for time series modeling")

if __name__ == "__main__":
    main()