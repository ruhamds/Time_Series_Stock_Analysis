"""
Utility functions for financial analysis
Contains reusable functions for calculations and analysis
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_returns(prices):
    """
    Calculate daily returns from price series
    
    Args:
        prices (pd.Series): Price time series
    
    Returns:
        pd.Series: Daily returns
    """
    return prices.pct_change()

def calculate_rolling_volatility(returns, window=20):
    """
    Calculate rolling volatility
    
    Args:
        returns (pd.Series): Return time series
        window (int): Rolling window size
    
    Returns:
        pd.Series: Rolling volatility
    """
    return returns.rolling(window).std()

def calculate_var(returns, confidence_level=0.05):
    """
    Calculate Value at Risk using historical simulation
    
    Args:
        returns (pd.Series): Return time series
        confidence_level (float): Confidence level (0.05 = 5% VaR)
    
    Returns:
        float: VaR value as positive number
    """
    if len(returns.dropna()) == 0:
        return np.nan
    return -np.percentile(returns.dropna(), confidence_level * 100)

def calculate_cvar(returns, confidence_level=0.05):
    """
    Calculate Conditional Value at Risk
    
    Args:
        returns (pd.Series): Return time series
        confidence_level (float): Confidence level
    
    Returns:
        float: CVaR value
    """
    if len(returns.dropna()) == 0:
        return np.nan
    
    var_threshold = np.percentile(returns.dropna(), confidence_level * 100)
    return -returns[returns <= var_threshold].mean()

def calculate_sharpe_ratio(returns, risk_free_rate=0.03/252):
    """
    Calculate Sharpe Ratio
    
    Args:
        returns (pd.Series): Return time series
        risk_free_rate (float): Daily risk-free rate
    
    Returns:
        float: Sharpe ratio
    """
    if len(returns.dropna()) == 0:
        return np.nan
    
    excess_returns = returns.dropna() - risk_free_rate
    if excess_returns.std() == 0:
        return 0
    return excess_returns.mean() / excess_returns.std()

def calculate_max_drawdown(prices):
    """
    Calculate maximum drawdown
    
    Args:
        prices (pd.Series): Price time series
    
    Returns:
        float: Maximum drawdown as negative percentage
    """
    cumulative = (1 + prices.pct_change().fillna(0)).cumprod()
    running_max = cumulative.expanding().max()
    drawdown = (cumulative - running_max) / running_max
    return drawdown.min()

def perform_adf_test(series, title="Series"):
    """
    Perform Augmented Dickey-Fuller test for stationarity
    
    Args:
        series (pd.Series): Time series to test
        title (str): Title for output
    
    Returns:
        dict: Test results
    """
    result = adfuller(series.dropna())
    
    output = {
        'title': title,
        'adf_statistic': result[0],
        'p_value': result[1],
        'critical_values': result[4],
        'is_stationary': result[1] <= 0.05
    }
    
    return output

def detect_outliers(returns, threshold=3):
    """
    Detect outliers in return series
    
    Args:
        returns (pd.Series): Return time series
        threshold (float): Number of standard deviations for threshold
    
    Returns:
        pd.Series: Outliers
    """
    std_dev = returns.std()
    outlier_threshold = threshold * std_dev
    return returns[abs(returns) > outlier_threshold]

def annualize_metrics(daily_metric, metric_type='return'):
    """
    Annualize daily metrics
    
    Args:
        daily_metric (float): Daily metric value
        metric_type (str): Type of metric ('return', 'volatility', 'sharpe')
    
    Returns:
        float: Annualized metric
    """
    if metric_type == 'return':
        return daily_metric * 252
    elif metric_type == 'volatility':
        return daily_metric * np.sqrt(252)
    elif metric_type == 'sharpe':
        return daily_metric * np.sqrt(252)
    else:
        return daily_metric

def create_summary_table(assets_data):
    """
    Create comprehensive summary table of metrics
    
    Args:
        assets_data (dict): Dictionary of asset dataframes
    
    Returns:
        pd.DataFrame: Summary table
    """
    summary = pd.DataFrame(index=list(assets_data.keys()))
    
    for ticker, data in assets_data.items():
        returns = data['Daily_Return'].dropna()
        
        # Basic metrics
        summary.loc[ticker, 'Annual Return (%)'] = annualize_metrics(returns.mean(), 'return') * 100
        summary.loc[ticker, 'Annual Volatility (%)'] = annualize_metrics(returns.std(), 'volatility') * 100
        summary.loc[ticker, 'Sharpe Ratio'] = annualize_metrics(calculate_sharpe_ratio(returns), 'sharpe')
        
        # Risk metrics
        summary.loc[ticker, 'Daily VaR 5% (%)'] = calculate_var(returns, 0.05) * 100
        summary.loc[ticker, 'Daily VaR 1% (%)'] = calculate_var(returns, 0.01) * 100
        summary.loc[ticker, 'Max Drawdown (%)'] = calculate_max_drawdown(data['Close']) * 100
        
        # Additional metrics
        summary.loc[ticker, 'Skewness'] = returns.skew()
        summary.loc[ticker, 'Kurtosis'] = returns.kurtosis()
    
    return summary.round(3)

def plot_price_comparison(assets_data, figsize=(15, 10)):
    """
    Plot price comparison for all assets
    
    Args:
        assets_data (dict): Dictionary of asset dataframes
        figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(len(assets_data), 1, figsize=figsize)
    if len(assets_data) == 1:
        axes = [axes]
    
    for i, (ticker, data) in enumerate(assets_data.items()):
        axes[i].plot(data.index, data['Close'], linewidth=1.5, label=f'{ticker} Close')
        if 'MA_20' in data.columns:
            axes[i].plot(data.index, data['MA_20'], linewidth=1, alpha=0.7, label=f'{ticker} 20-MA')
        
        axes[i].set_title(f'{ticker} Price Movement')
        axes[i].set_ylabel('Price ($)')
        axes[i].legend()
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_returns_comparison(assets_data, figsize=(15, 10)):
    """
    Plot returns comparison for all assets
    
    Args:
        assets_data (dict): Dictionary of asset dataframes
        figsize (tuple): Figure size
    """
    fig, axes = plt.subplots(len(assets_data), 1, figsize=figsize)
    if len(assets_data) == 1:
        axes = [axes]
    
    for i, (ticker, data) in enumerate(assets_data.items()):
        returns = data['Daily_Return'].dropna() * 100
        axes[i].plot(returns.index, returns, linewidth=0.8, alpha=0.7)
        axes[i].axhline(y=0, color='black', linestyle='-', alpha=0.3)
        axes[i].set_title(f'{ticker} Daily Returns')
        axes[i].set_ylabel('Return (%)')
        axes[i].grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def save_results(summary_df, filename='analysis_results.csv'):
    """
    Save analysis results to CSV
    
    Args:
        summary_df (pd.DataFrame): Summary dataframe
        filename (str): Output filename
    """
    summary_df.to_csv(filename)
    print(f"Results saved to {filename}")