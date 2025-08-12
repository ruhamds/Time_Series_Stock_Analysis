# Time Series Analysis - Task 1

## Project Overview
This project analyzes historical financial data for three key assets (TSLA, BND, SPY) to support portfolio management decisions. The analysis covers the period from July 1, 2015, to July 31, 2025.

## Assets Analyzed
- **TSLA (Tesla Inc.)**: High-growth stock with high volatility
- **BND (Vanguard Total Bond Market ETF)**: Bond ETF providing stability and low risk
- **SPY (SPDR S&P 500 ETF)**: ETF tracking S&P 500 for broad market exposure

## Project Structure

### Core Scripts
```
├── data_loading.py          # Fetches data from yfinance API
├── config.py               # Project configuration and parameters
├── utils.py                # Utility functions for calculations
├── main_analysis.py        # Main execution script
```

### Analysis Notebooks
```
├── EDA.ipynb              # Comprehensive exploratory data analysis
├── metrics.ipynb          # Risk metrics and performance analysis
```

### Data and Outputs
```
├── data/                  # Stored CSV data files
├── outputs/              # Analysis results and reports
├── figures/              # Generated visualizations
```

## How to Run the Analysis

### Step 1: Install Required Libraries
```python
pip install yfinance pandas numpy matplotlib seaborn scipy statsmodels
```

### Step 2: Run Data Loading
```python
python data_loading.py
```
This script will:
- Fetch historical data for TSLA, BND, and SPY
- Save data to CSV files in the `data/` folder
- Display basic data information

### Step 3: Run Complete Analysis
```python
python main_analysis.py
```
This script orchestrates the entire Task 1 analysis:
- Loads and cleans data
- Performs exploratory data analysis
- Calculates risk metrics
- Generates summary reports

### Step 4: Detailed Analysis (Optional)
Open and run the Jupyter notebooks:
- `EDA.ipynb` for detailed visualizations and insights
- `metrics.ipynb` for comprehensive risk analysis

## Analysis Components

### 1. Data Preprocessing
- **Purpose**: Clean and prepare data for analysis
- **Methods**: Handle missing values, calculate returns, add technical indicators
- **Outputs**: Clean datasets with additional features

### 2. Exploratory Data Analysis
- **Purpose**: Understand data characteristics and patterns
- **Methods**: Time series plots, distribution analysis, trend identification
- **Key Insights**: Price movements, volatility patterns, market events

### 3. Stationarity Testing
- **Purpose**: Test if data is suitable for time series modeling
- **Methods**: Augmented Dickey-Fuller test on prices and returns
- **Findings**: Prices are non-stationary, returns are stationary

### 4. Risk Metrics Calculation
- **Value at Risk (VaR)**: Potential losses under normal conditions
- **Conditional VaR**: Average loss beyond VaR threshold
- **Sharpe Ratio**: Risk-adjusted return measure
- **Maximum Drawdown**: Largest peak-to-trough decline

### 5. Outlier Detection
- **Purpose**: Identify extreme market movements
- **Methods**: Statistical threshold (±3 standard deviations)
- **Applications**: Risk management and event analysis

### 6. Correlation Analysis
- **Purpose**: Understand how assets move together
- **Methods**: Pearson correlation of daily returns
- **Portfolio Implications**: Diversification opportunities

## Key Findings

### Asset Characteristics
- **TSLA**: High return potential (15%+ annual) but very high risk (40%+ volatility)
- **BND**: Low risk (3-5% volatility) with stable returns (2-4% annual)
- **SPY**: Balanced profile (10-12% returns, 15-20% volatility)

### Risk-Return Profile
- TSLA offers growth but increases portfolio risk significantly
- BND provides stability and reduces overall volatility
- SPY delivers market-level performance with moderate risk

### Correlation Insights
- TSLA and SPY show moderate positive correlation (0.4-0.6)
- BND has low correlation with stocks (0.0-0.2)
- Combining all three enables effective diversification

## Output Files

### Generated Files
- `task1_summary_results.csv`: Complete metrics summary
- `correlation_matrix.csv`: Asset correlation matrix
- `TICKER_data.csv`: Individual asset data files

### Key Metrics Included
- Annual returns and volatility
- Sharpe ratios
- Value at Risk (1% and 5% levels)
- Maximum drawdown
- Statistical properties (skewness, kurtosis)

## Next Steps
1. Review generated summary files and metrics
2. Run visualization notebooks for detailed insights
3. Proceed to Task 2 for time series forecasting models
4. Use insights for portfolio optimization in Task 4

## Dependencies
- pandas: Data manipulation and analysis
- numpy: Numerical computations
- yfinance: Financial data fetching
- matplotlib/seaborn: Visualization
- scipy: Statistical functions
- statsmodels: Time series analysis

## Notes
- Data is fetched from Yahoo Finance (yfinance)
- All calculations use standard financial formulas
- Code is designed to be human-readable and well-documented
- Results provide foundation for portfolio optimization decisions

## Author
Financial Analysis for GMF Investments Portfolio Management