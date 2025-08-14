"""
Forecast Visualization Script
Creates visualizations for LSTM forecast results and portfolio implications
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Your LSTM forecast results
FORECAST_DATA = {
    'current_price': 319.04,
    'forecast_price': 205.52,
    'forecast_high': 301.93,
    'forecast_low': 205.52,
    'expected_return': -0.356,
    'forecast_period_months': 6
}

def plot_forecast_scenario():
    """
    Create a visualization of the forecast scenario
    """
    print("Creating forecast scenario visualization...")
    
    # Create dates for visualization
    current_date = datetime.now()
    forecast_date = current_date + timedelta(days=180)  # 6 months
    
    # Create price path simulation
    dates = pd.date_range(start=current_date, end=forecast_date, freq='D')
    
    # Simple linear decline for visualization (actual LSTM would be more complex)
    n_days = len(dates)
    price_path = np.linspace(FORECAST_DATA['current_price'], FORECAST_DATA['forecast_price'], n_days)
    
    # Add some realistic volatility around the trend
    np.random.seed(42)
    volatility = 0.03  # 3% daily volatility
    daily_returns = np.random.normal(0, volatility, n_days-1)
    
    # Adjust returns to end at forecast price
    adjustment_factor = (FORECAST_DATA['forecast_price'] / FORECAST_DATA['current_price'] - 1) / (n_days-1)
    daily_returns = daily_returns + adjustment_factor
    
    # Calculate price path with volatility
    realistic_path = [FORECAST_DATA['current_price']]
    for ret in daily_returns:
        realistic_path.append(realistic_path[-1] * (1 + ret))
    
    # Ensure we end at forecast price
    realistic_path[-1] = FORECAST_DATA['forecast_price']
    
    # Create the plot
    plt.figure(figsize=(14, 10))
    
    # Plot 1: Price forecast with confidence interval
    plt.subplot(2, 2, 1)
    plt.plot(dates, realistic_path, 'b-', linewidth=2, label='LSTM Forecast Path')
    plt.axhline(y=FORECAST_DATA['current_price'], color='green', linestyle='--', alpha=0.7, label='Current Price')
    plt.axhline(y=FORECAST_DATA['forecast_price'], color='red', linestyle='--', alpha=0.7, label='Target Price')
    
    # Add confidence interval
    upper_bound = np.linspace(FORECAST_DATA['current_price'], FORECAST_DATA['forecast_high'], n_days)
    lower_bound = np.linspace(FORECAST_DATA['current_price'], FORECAST_DATA['forecast_low'], n_days)
    plt.fill_between(dates, lower_bound, upper_bound, alpha=0.2, color='blue', label='Confidence Interval')
    
    plt.title('TSLA 6-Month Price Forecast', fontweight='bold', fontsize=14)
    plt.ylabel('Price ($)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    
    # Plot 2: Return distribution scenarios
    plt.subplot(2, 2, 2)
    scenarios = ['Best Case', 'Expected', 'Worst Case']
    returns = [
        (FORECAST_DATA['forecast_high'] - FORECAST_DATA['current_price']) / FORECAST_DATA['current_price'] * 100,
        FORECAST_DATA['expected_return'] * 100,
        (FORECAST_DATA['forecast_low'] - FORECAST_DATA['current_price']) / FORECAST_DATA['current_price'] * 100
    ]
    colors = ['green', 'orange', 'red']
    
    bars = plt.bar(scenarios, returns, color=colors, alpha=0.7)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.5)
    plt.title('TSLA 6-Month Return Scenarios', fontweight='bold', fontsize=14)
    plt.ylabel('Return (%)')
    plt.grid(True, alpha=0.3, axis='y')
    
    # Add value labels on bars
    for bar, return_val in zip(bars, returns):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + (1 if return_val > 0 else -3),
                f'{return_val:.1f}%', ha='center', va='bottom' if return_val > 0 else 'top', fontweight='bold')
    
    # Plot 3: Risk comparison with other assets
    plt.subplot(2, 2, 3)
   # Plot 3: Risk comparison with other assets
plt.subplot(2, 2, 3)
try:
    # Load other assets for comparison
    bnd = pd.read_csv('data/BND_data.csv', index_col=0, parse_dates=True)
    spy = pd.read_csv('data/SPY_data.csv', index_col=0, parse_dates=True)
    
    # Calculate historical volatilities (annualized)
    bnd_vol = bnd['Close'].pct_change().std() * np.sqrt(252) * 100
    spy_vol = spy['Close'].pct_change().std() * np.sqrt(252) * 100
    tsla_vol = 40  # Approximate based on TSLA historical volatility
    
    assets = ['BND', 'SPY', 'TSLA']
    volatilities = [bnd_vol, spy_vol, tsla_vol]
    expected_returns_comp = [3, 10, FORECAST_DATA['expected_return'] * 100]  # percent
    
    # Create a scatter plot: Volatility vs Expected Return
    plt.scatter(volatilities, expected_returns_comp, color=['blue','orange','red'], s=100)
    for i, asset in enumerate(assets):
        plt.text(volatilities[i]+0.2, expected_returns_comp[i], asset, fontsize=12, fontweight='bold')
    
    plt.xlabel('Annualized Volatility (%)')
    plt.ylabel('Expected Return (%)')
    plt.title('Risk vs Return Comparison', fontweight='bold', fontsize=14)
    plt.grid(True, alpha=0.3)

except FileNotFoundError:
    plt.text(0.5, 0.5, 'BND/SPY data not found', ha='center', va='center', fontsize=12)
    plt.title('Risk vs Return Comparison', fontweight='bold', fontsize=14)
    plt.axis('off')
