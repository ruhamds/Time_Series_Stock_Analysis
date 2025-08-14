"""
Task 4: Portfolio Optimization Using LSTM Forecast
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
import warnings
warnings.filterwarnings('ignore')

# Your LSTM forecast results
TSLA_FORECAST_RETURN = -0.356  # -35.6% over 6 months

def load_and_prepare_data():
    """
    Load historical data and prepare inputs for optimization
    """
    print("=== LOADING AND PREPARING DATA ===")
    
    try:
        # Load historical data
        tsla = pd.read_csv('data/TSLA_data.csv', index_col=0, parse_dates=True)
        bnd = pd.read_csv('data/BND_data.csv', index_col=0, parse_dates=True)
        spy = pd.read_csv('data/SPY_data.csv', index_col=0, parse_dates=True)
        
        # Calculate returns if not present
        assets_data = {'TSLA': tsla, 'BND': bnd, 'SPY': spy}
        for name, data in assets_data.items():
            if 'Daily_Return' not in data.columns:
                data['Daily_Return'] = data['Close'].pct_change()
        
        print("✓ Data loaded successfully")
        return assets_data
        
    except FileNotFoundError:
        print("Error: Data files not found. Please run data_loading.py first.")
        return None

def calculate_expected_returns(assets_data):
    """
    Calculate expected returns for portfolio optimization
    TSLA: Use LSTM forecast
    BND & SPY: Use historical averages
    """
    print("\n=== CALCULATING EXPECTED RETURNS ===")
    
    expected_returns = {}
    
    # TSLA: Use your LSTM forecast (annualized)
    tsla_annual = TSLA_FORECAST_RETURN * 2  # Convert 6-month to annual (rough)
    expected_returns['TSLA'] = tsla_annual
    print(f"TSLA: {tsla_annual*100:.2f}% (from LSTM forecast)")
    
    # BND and SPY: Historical averages
    for ticker in ['BND', 'SPY']:
        daily_returns = assets_data[ticker]['Daily_Return'].dropna()
        annual_return = daily_returns.mean() * 252
        expected_returns[ticker] = annual_return
        print(f"{ticker}: {annual_return*100:.2f}% (historical average)")
    
    return pd.Series(expected_returns)

def calculate_covariance_matrix(assets_data):
    """
    Calculate covariance matrix from historical returns
    """
    print("\n=== CALCULATING COVARIANCE MATRIX ===")
    
    # Combine daily returns
    returns_df = pd.DataFrame({
        'TSLA': assets_data['TSLA']['Daily_Return'],
        'BND': assets_data['BND']['Daily_Return'],
        'SPY': assets_data['SPY']['Daily_Return']
    }).dropna()
    
    # Annualized covariance matrix
    cov_matrix = returns_df.cov() * 252
    
    print("Correlation Matrix:")
    print(returns_df.corr().round(3))
    
    return cov_matrix

def portfolio_metrics(weights, expected_returns, cov_matrix):
    """
    Calculate portfolio return and risk
    """
    portfolio_return = np.sum(expected_returns * weights)
    portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return portfolio_return, portfolio_risk

def negative_sharpe_ratio(weights, expected_returns, cov_matrix, risk_free_rate=0.03):
    """
    Calculate negative Sharpe ratio for minimization
    """
    port_return, port_risk = portfolio_metrics(weights, expected_returns, cov_matrix)
    if port_risk == 0:
        return -np.inf
    sharpe = (port_return - risk_free_rate) / port_risk
    return -sharpe

def minimize_variance(weights, expected_returns, cov_matrix):
    """
    Minimize portfolio variance
    """
    _, port_risk = portfolio_metrics(weights, expected_returns, cov_matrix)
    return port_risk

def optimize_portfolios(expected_returns, cov_matrix):
    """
    Find optimal portfolios using different objectives
    """
    print("\n=== OPTIMIZING PORTFOLIOS ===")
    
    n_assets = len(expected_returns)
    
    # Constraints and bounds
    constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
    bounds = tuple((0, 1) for _ in range(n_assets))
    initial_guess = np.array([1/n_assets] * n_assets)
    
    # 1. Maximum Sharpe Ratio Portfolio
    print("Optimizing for Maximum Sharpe Ratio...")
    max_sharpe_result = minimize(
        negative_sharpe_ratio, initial_guess,
        args=(expected_returns, cov_matrix),
        method='SLSQP', bounds=bounds, constraints=constraints
    )
    max_sharpe_weights = max_sharpe_result.x
    
    # 2. Minimum Variance Portfolio
    print("Optimizing for Minimum Variance...")
    min_var_result = minimize(
        minimize_variance, initial_guess,
        args=(expected_returns, cov_matrix),
        method='SLSQP', bounds=bounds, constraints=constraints
    )
    min_var_weights = min_var_result.x
    
    return max_sharpe_weights, min_var_weights

def generate_efficient_frontier(expected_returns, cov_matrix, num_portfolios=100):
    """
    Generate efficient frontier
    """
    print("Generating Efficient Frontier...")
    
    n_assets = len(expected_returns)
    results = []
    
    # Define target returns range
    min_ret = expected_returns.min()
    max_ret = expected_returns.max()
    target_returns = np.linspace(min_ret, max_ret, num_portfolios)
    
    for target_ret in target_returns:
        # Constraints for target return
        constraints = [
            {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
            {'type': 'eq', 'fun': lambda x, target=target_ret: np.sum(expected_returns * x) - target}
        ]
        bounds = tuple((0, 1) for _ in range(n_assets))
        initial_guess = np.array([1/n_assets] * n_assets)
        
        try:
            result = minimize(
                minimize_variance, initial_guess,
                args=(expected_returns, cov_matrix),
                method='SLSQP', bounds=bounds, constraints=constraints
            )
            
            if result.success:
                weights = result.x
                port_return, port_risk = portfolio_metrics(weights, expected_returns, cov_matrix)
                results.append([port_return, port_risk, weights])
        except:
            continue
    
    return results

def plot_efficient_frontier(efficient_frontier, max_sharpe_weights, min_var_weights, expected_returns, cov_matrix):
    """
    Plot the efficient frontier with optimal portfolios
    """
    print("\n=== CREATING EFFICIENT FRONTIER PLOT ===")
    
    if not efficient_frontier:
        print("No efficient frontier data available")
        return
    
    # Extract returns and risks
    frontier_returns = [result[0] for result in efficient_frontier]
    frontier_risks = [result[1] for result in efficient_frontier]
    
    # Calculate metrics for optimal portfolios
    max_sharpe_return, max_sharpe_risk = portfolio_metrics(max_sharpe_weights, expected_returns, cov_matrix)
    min_var_return, min_var_risk = portfolio_metrics(min_var_weights, expected_returns, cov_matrix)
    
    # Create plot
    plt.figure(figsize=(12, 8))
    
    # Plot efficient frontier
    plt.plot(frontier_risks, frontier_returns, 'b-', linewidth=2, label='Efficient Frontier')
    
    # Plot optimal portfolios
    plt.scatter(max_sharpe_risk, max_sharpe_return, marker='*', s=500, c='red', 
               label='Max Sharpe Ratio', zorder=3)
    plt.scatter(min_var_risk, min_var_return, marker='*', s=500, c='green', 
               label='Min Variance', zorder=3)
    
    # Plot individual assets
    for i, asset in enumerate(expected_returns.index):
        asset_return = expected_returns[asset]
        asset_risk = np.sqrt(cov_matrix.iloc[i, i])
        plt.scatter(asset_risk, asset_return, marker='o', s=100, alpha=0.7, 
                   label=f'{asset}')
    
    plt.xlabel('Annual Risk (Standard Deviation)', fontsize=12)
    plt.ylabel('Annual Expected Return', fontsize=12)
    plt.title('Efficient Frontier with LSTM Forecast for TSLA', fontsize=16, fontweight='bold')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('efficient_frontier.png', dpi=300, bbox_inches='tight')
    plt.show()
    print("Efficient frontier saved as 'efficient_frontier.png'")

def display_portfolio_results(max_sharpe_weights, min_var_weights, expected_returns, cov_matrix):
    """
    Display detailed results for optimal portfolios
    """
    print("\n" + "="*60)
    print("PORTFOLIO OPTIMIZATION RESULTS")
    print("="*60)
    
    assets = expected_returns.index
    
    # Maximum Sharpe Ratio Portfolio
    print("\n1. MAXIMUM SHARPE RATIO PORTFOLIO")
    print("-" * 45)
    
    max_sharpe_return, max_sharpe_risk = portfolio_metrics(max_sharpe_weights, expected_returns, cov_matrix)
    max_sharpe_sharpe = (max_sharpe_return - 0.03) / max_sharpe_risk
    
    print("Asset Allocations:")
    for i, asset in enumerate(assets):
        print(f"  {asset}: {max_sharpe_weights[i]*100:.1f}%")
    
    print(f"\nPortfolio Metrics:")
    print(f"  Expected Annual Return: {max_sharpe_return*100:.2f}%")
    print(f"  Annual Volatility: {max_sharpe_risk*100:.2f}%")
    print(f"  Sharpe Ratio: {max_sharpe_sharpe:.3f}")
    
    # Minimum Variance Portfolio
    print(f"\n2. MINIMUM VARIANCE PORTFOLIO")
    print("-" * 40)
    
    min_var_return, min_var_risk = portfolio_metrics(min_var_weights, expected_returns, cov_matrix)
    min_var_sharpe = (min_var_return - 0.03) / min_var_risk
    
    print("Asset Allocations:")
    for i, asset in enumerate(assets):
        print(f"  {asset}: {min_var_weights[i]*100:.1f}%")
    
    print(f"\nPortfolio Metrics:")
    print(f"  Expected Annual Return: {min_var_return*100:.2f}%")
    print(f"  Annual Volatility: {min_var_risk*100:.2f}%")
    print(f"  Sharpe Ratio: {min_var_sharpe:.3f}")

def save_optimization_results(max_sharpe_weights, min_var_weights, expected_returns, cov_matrix):
    """
    Save optimization results to files
    """
    print(f"\n=== SAVING RESULTS ===")
    
    assets = expected_returns.index
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'Asset': assets,
        'Expected_Return': expected_returns.values,
        'Max_Sharpe_Weight': max_sharpe_weights,
        'Min_Var_Weight': min_var_weights
    })
    
    # Add portfolio metrics
    max_sharpe_return, max_sharpe_risk = portfolio_metrics(max_sharpe_weights, expected_returns, cov_matrix)
    min_var_return, min_var_risk = portfolio_metrics(min_var_weights, expected_returns, cov_matrix)
    
    summary = {
        'Portfolio Type': ['Max Sharpe Ratio', 'Min Variance'],
        'Expected Return (%)': [max_sharpe_return*100, min_var_return*100],
        'Volatility (%)': [max_sharpe_risk*100, min_var_risk*100],
        'Sharpe Ratio': [(max_sharpe_return-0.03)/max_sharpe_risk, (min_var_return-0.03)/min_var_risk]
    }
    
    results_df.to_csv('portfolio_weights.csv', index=False)
    pd.DataFrame(summary).to_csv('portfolio_summary.csv', index=False)
    
    print("Results saved to:")
    print("• portfolio_weights.csv - Asset allocations")
    print("• portfolio_summary.csv - Portfolio metrics")

def main():
    """
    Main portfolio optimization workflow
    """
    print("="*60)
    print("TASK 4: PORTFOLIO OPTIMIZATION")
    print("Using LSTM Forecast for TSLA")
    print("="*60)
    
    # Step 1: Load data
    assets_data = load_and_prepare_data()
    if not assets_data:
        return
    
    # Step 2: Calculate expected returns
    expected_returns = calculate_expected_returns(assets_data)
    
    # Step 3: Calculate covariance matrix
    cov_matrix = calculate_covariance_matrix(assets_data)
    
    # Step 4: Optimize portfolios
    max_sharpe_weights, min_var_weights = optimize_portfolios(expected_returns, cov_matrix)
    
    # Step 5: Generate efficient frontier
    efficient_frontier = generate_efficient_frontier(expected_returns, cov_matrix)
    
    # Step 6: Create visualizations
    plot_efficient_frontier(efficient_frontier, max_sharpe_weights, min_var_weights, expected_returns, cov_matrix)
    
    # Step 7: Display results
    display_portfolio_results(max_sharpe_weights, min_var_weights, expected_returns, cov_matrix)
    
    # Step 8: Save results
    save_optimization_results(max_sharpe_weights, min_var_weights, expected_returns, cov_matrix)
    
    print(f"\n" + "="*60)
    print("PORTFOLIO OPTIMIZATION COMPLETED!")
    print("="*60)
    print("\nKey Findings:")
    print("• TSLA's negative forecast significantly impacts optimal allocation")
    print("• Portfolio optimization favors defensive assets (BND)")
    print("• Maximum Sharpe ratio portfolio likely has minimal TSLA exposure")
    print("• Results demonstrate impact of forecasting on portfolio construction")

if __name__ == "__main__":
    main()