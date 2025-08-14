
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
print("\nCovariance Matrix:")
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

print("\n=== OPTIMAL PORTFOLIO WEIGHTS ===")
for i, asset in enumerate(assets):
    print(f"{asset}: {optimal_weights[i]*100:.1f}%")

# Calculate portfolio metrics
port_return, port_risk = portfolio_performance(optimal_weights, expected_returns, covariance_matrix)
sharpe_ratio = (port_return - 0.03) / port_risk

print(f"\nOptimal Portfolio Metrics:")
print(f"Expected Annual Return: {port_return*100:.2f}%")
print(f"Annual Volatility: {port_risk*100:.2f}%")
print(f"Sharpe Ratio: {sharpe_ratio:.3f}")
