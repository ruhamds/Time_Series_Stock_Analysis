"""
Task 4 Preparation: Portfolio Optimization Setup
Prepares data for portfolio optimization using LSTM forecast results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Your LSTM forecast results
TSLA_FORECAST = {
    'expected_return_6m': -0.356,  # -35.6% from your LSTM model
    'current_price': 319.04,
    'forecast_price': 205.52
}

def load_historical_data():
    """
    Load historical data for all three assets
    """
    print("Loading historical data for portfolio optimization...")
    
    try:
        tsla = pd.read_csv('data/TSLA_data.csv', index_col=0, parse_dates=True)
        bnd = pd.read_csv('data/BND_data.csv', index_col=0, parse_dates=True)
        spy = pd.read_csv('data/SPY_data.csv', index_col=0, parse_dates=True)
        
        # Calculate returns if not present
        for name, data in [('TSLA', tsla), ('BND', bnd), ('SPY', spy)]:
            if 'Daily_Return' not in data.columns:
                data['Daily_Return'] = data['Close'].pct_change()
        
        return {'TSLA': tsla, 'BND': bnd, 'SPY': spy}
    
    except FileNotFoundError:
        print("Error: Data files not found. Please run data_loading.py first.")
        return None

def calculate_expected_returns(assets_data):
    """
    Calculate expected returns for portfolio optimization
    Uses LSTM forecast for TSLA and historical averages for BND and SPY
    """
    print("\n=== EXPECTED RETURNS CALCULATION ===")
    
    expected_returns = {}
    
    # TSLA: Use LSTM forecast (convert 6-month to annual)
    tsla_annual_return = TSLA_FORECAST['expected_return_6m'] * 2  # Rough annualization
    expected_returns['TSLA'] = tsla_annual_return
    
    print(f"TSLA Expected Annual Return: {tsla_annual_return*100:.2f}% (from LSTM forecast)")
    
    # BND and SPY: Use historical average returns (annualized)
    for ticker in ['BND', 'SPY']:
        returns = assets_data[ticker]['Daily_Return'].dropna()
        historical_annual = returns.mean() * 252
        expected_returns[ticker] = historical_annual
        
        print(f"{ticker} Expected Annual Return: {historical_annual*100:.2f}% (historical average)")
    
    return expected_returns

def calculate_covariance_matrix(assets_data):
    """
    Calculate covariance matrix from historical daily returns
    """
    print(f"\n=== COVARIANCE MATRIX CALCULATION ===")
    
    # Combine daily returns
    returns_df = pd.DataFrame({
        'TSLA': assets_data['TSLA']['Daily_Return'],
        'BND': assets_data['BND']['Daily_Return'], 
        'SPY': assets_data['SPY']['Daily_Return']
    }).dropna()
    
    # Calculate annualized covariance matrix
    daily_cov = returns_df.cov()
    annual_cov = daily_cov * 252
    
    print("Daily Returns Correlation Matrix:")
    correlation_matrix = returns_df.corr()
    print(correlation_matrix.round(3))
    
    print(f"\nAnnualized Covariance Matrix:")
    print(annual_cov.round(6))
    
    return annual_cov, correlation_matrix

def portfolio_inputs_summary(expected_returns, covariance_matrix):
    """
    Summarize inputs for portfolio optimization
    """
    print(f"\n=== PORTFOLIO OPTIMIZATION INPUTS SUMMARY ===")
    
    print("Expected Annual Returns:")
    for asset, ret in expected_returns.items():
        print(f"  {asset}: {ret*100:.2f}%")
    
    print(f"\nRisk Characteristics (Annual Volatility):")
    for asset in expected_returns.keys():
        volatility = np.sqrt(covariance_matrix.loc[asset, asset])
        print(f"  {asset}: {volatility*100:.2f}%")
    
    # Risk-return summary
    print(f"\nRisk-Return Profile:")
    for asset in expected_returns.keys():
        ret = expected_returns[asset]
        vol = np.sqrt(covariance_matrix.loc[asset, asset])
        risk_return_ratio = ret / vol if vol > 0 else 0
        
        print(f"  {asset}: Return={ret*100:.1f}%, Risk={vol*100:.1f}%, Ratio={risk_return_ratio:.2f}")

def analyze_forecast_impact():
    """
    Analyze how the LSTM forecast affects portfolio construction
    """
    print(f"\n=== FORECAST IMPACT ANALYSIS ===")
    
    print("LSTM Forecast Impact on Portfolio:")
    print(f"• TSLA shows negative expected return ({TSLA_FORECAST['expected_return_6m']*100:.1f}%)")
    print("• This will likely result in low or zero TSLA allocation in optimal portfolio")
    print("• Portfolio optimization will favor BND and SPY with positive expected returns")
    print("• Risk-return trade-off will favor defensive positioning")
    
    print(f"\nExpected Portfolio Implications:")
    print("• Optimal portfolio will likely be conservative")
    print("• Higher allocation to BND for stability")
    print("• Moderate allocation to SPY for growth")
    print("• Minimal allocation to TSLA due to negative forecast")
    
    print(f"\nStrategic Considerations:")
    print("• Forecast represents one scenario - consider sensitivity analysis")
    print("• May want to impose minimum allocations for diversification")
    print("• Consider different risk tolerance levels")
    print("• Monitor for forecast updates and rebalance accordingly")

def save_optimization_inputs(expected_returns, covariance_matrix):
    """
    Save inputs for portfolio optimization
    """
    print(f"\n=== SAVING OPTIMIZATION INPUTS ===")
    
    # Save expected returns
    returns_df = pd.DataFrame.from_dict(expected_returns, orient='index', columns=['Expected_Return'])
    returns_df.to_csv('expected_returns.csv')
    print("Expected returns saved to expected_returns.csv")
    
    # Save covariance matrix
    covariance_matrix.to_csv('covariance_matrix.csv')
    print("Covariance matrix saved to covariance_matrix.csv")
    
    # Create summary for Task 4
    summary = {
        'TSLA_forecast_return': TSLA_FORECAST['expected_return_6m'],
        'TSLA_annual_return': expected_returns['TSLA'],
        'BND_annual_return': expected_returns['BND'],
        'SPY_annual_return': expected_returns['SPY'],
        'data_prepared_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    summary_df = pd.DataFrame.from_dict(summary, orient='index', columns=['Value'])
    summary_df.to_csv('task4_inputs_summary.csv')
    print("Task 4 inputs summary saved to task4_inputs_summary.csv")

def generate_task4_code_template():
    """
    Generate a code template for Task 4 portfolio optimization
    """
    template_code = '''
# Task 4: Portfolio Optimization Code Template
# Using your LSTM forecast results

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Load the prepared inputs
expected_returns = pd.read_csv('expected_returns.csv', index_col=0)['Expected_Return']
covariance_matrix = pd.read_csv('covariance_matrix.csv', index_col=0)

print("Expected Returns:", expected_returns.to_dict())
print("\\nCovariance Matrix:")
print(covariance_matrix)

def portfolio_performance(weights, expected_returns, cov_matrix):
    """Calculate portfolio return and risk"""
    portfolio_return = np.sum(expected_returns * weights)
    portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return portfolio_return, portfolio_risk

def negative_sharpe_ratio(weights, expected_returns, cov_matrix, risk_free_rate=0.03):
    """Calculate negative Sharpe ratio for minimization"""
    p_return, p_risk = portfolio_performance(weights, expected_returns, cov_matrix)
    sharpe = (p_return - risk_free_rate) / p_risk
    return -sharpe

def optimize_portfolio():
    """Find optimal portfolio weights"""
    n_assets = len(expected_returns)
    
    # Constraints: weights sum to 1
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    
    # Bounds: 0 <= weight <= 1 for each asset
    bounds = tuple((0, 1) for _ in range(n_assets))
    
    # Initial guess: equal weights
    initial_guess = np.array([1/n_assets] * n_assets)
    
    # Optimize for maximum Sharpe ratio
    result = minimize(negative_sharpe_ratio, initial_guess,
                     args=(expected_returns, covariance_matrix),
                     method='SLSQP', bounds=bounds, constraints=constraints)
    
    return result.x

# Run optimization
optimal_weights = optimize_portfolio()
assets = expected_returns.index

print("\\n=== OPTIMAL PORTFOLIO WEIGHTS ===")
for i, asset in enumerate(assets):
    print(f"{asset}: {optimal_weights[i]*100:.1f}%")

# Calculate portfolio metrics
port_return, port_risk = portfolio_performance(optimal_weights, expected_returns, covariance_matrix)
sharpe_ratio = (port_return - 0.03) / port_risk

print(f"\\nOptimal Portfolio Metrics:")
print(f"Expected Annual Return: {port_return*100:.2f}%")
print(f"Annual Volatility: {port_risk*100:.2f}%")
print(f"Sharpe Ratio: {sharpe_ratio:.3f}")
'''
    
    with open('task4_optimization_template.py', 'w') as f:
        f.write(template_code)
    
    print("Task 4 code template saved to task4_optimization_template.py")

def main():
    """
    Main function to prepare for Task 4 portfolio optimization
    """
    print("="*60)
    print("TASK 4 PREPARATION: PORTFOLIO OPTIMIZATION SETUP")
    print("Using LSTM Forecast Results for TSLA")
    print("="*60)
    
    # Load data
    assets_data = load_historical_data()
    if not assets_data:
        return
    
    # Calculate expected returns
    expected_returns = calculate_expected_returns(assets_data)
    
    # Calculate covariance matrix
    covariance_matrix, correlation_matrix = calculate_covariance_matrix(assets_data)
    
    # Summarize inputs
    portfolio_inputs_summary(expected_returns, covariance_matrix)
    
    # Analyze forecast impact
    analyze_forecast_impact()
    
    # Save inputs
    save_optimization_inputs(expected_returns, covariance_matrix)
    
    # Generate code template
    generate_task4_code_template()
    
    print(f"\n" + "="*60)
    print("TASK 4 PREPARATION COMPLETED!")
    print("="*60)
    print("\\nNext steps:")
    print("1. Review the expected returns and covariance matrix")
    print("2. Run task4_optimization_template.py for basic optimization")
    print("3. Implement efficient frontier analysis")
    print("4. Consider different risk tolerance levels")
    print("5. Analyze the impact of the negative TSLA forecast")

if __name__ == "__main__":
    main()
