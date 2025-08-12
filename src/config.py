"""
Configuration file for Portfolio Management Analysis
Contains all project settings and parameters
"""

# Data Configuration
DATA_CONFIG = {
    'tickers': ['TSLA', 'BND', 'SPY'],
    'start_date': '2015-07-01',
    'end_date': '2025-07-31',
    'data_folder': 'data'
}

# Asset Information
ASSET_INFO = {
    'TSLA': {
        'name': 'Tesla Inc.',
        'type': 'High-growth stock',
        'sector': 'Consumer Discretionary',
        'description': 'High returns with high volatility'
    },
    'BND': {
        'name': 'Vanguard Total Bond Market ETF',
        'type': 'Bond ETF',
        'sector': 'Fixed Income',
        'description': 'Stability and low risk'
    },
    'SPY': {
        'name': 'SPDR S&P 500 ETF',
        'type': 'Market ETF',
        'sector': 'Diversified',
        'description': 'Broad market exposure'
    }
}

# Analysis Parameters
ANALYSIS_CONFIG = {
    'rolling_window': 20,
    'volatility_window': 252,
    'var_confidence_levels': [0.01, 0.05],
    'risk_free_rate': 0.03,  # 3% annual
    'trading_days_per_year': 252
}

# Visualization Settings
PLOT_CONFIG = {
    'figure_size': (15, 10),
    'style': 'default',
    'colors': ['#1f77b4', '#ff7f0e', '#2ca02c'],
    'dpi': 100
}

# File Paths
PATHS = {
    'data_folder': 'data',
    'output_folder': 'outputs',
    'figures_folder': 'figures'
}