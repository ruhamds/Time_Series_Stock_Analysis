Time Series Stock Analysis Project
📌 Project Overview

This project focuses on analyzing historical financial data, forecasting stock prices, and constructing an optimized investment portfolio using both statistical models (ARIMA) and machine learning models (LSTM). The project is structured into five tasks:

Task 1: Exploratory Data Analysis & Risk Assessment

Task 2: Model Selection & Evaluation (ARIMA)

Task 3: Advanced Forecasting with LSTM

Task 4: Portfolio Optimization

Task 5: Backtesting & Performance Evaluation

The analysis is performed on three key assets:

TSLA (Tesla Inc.) – High-growth, high-risk equity

BND (Vanguard Total Bond Market ETF) – Low-risk bond ETF

SPY (S&P 500 ETF) – Broad market exposure

Data range: July 1, 2015 – July 31, 2025 (10 years)

📂 Project Structure
Time_Series_Stock_Analysis/
├── Notebooks/
│   ├── Task1/   # EDA & risk analysis
│   ├── Task2/   # ARIMA modeling
│   ├── Task3/   # LSTM forecasting
│   ├── Task4/   # Portfolio optimization
│   └── Task5/   # Backtesting & performance
├── src/
│   ├── data_definition.py
│   ├── forecast_analysis.py
│   ├── forecast_visualize.py
│   ├── portfolio_optimization.py
│   └── portfolio_optimization_prep.py
├── .github/
│   └── workflows/
│       └── ci.yml   # CI pipeline for linting and notebook execution
├── data/            # Raw and processed datasets
├── outputs/         # Generated reports and metrics
├── requirements.txt # Python dependencies
└── README.md        # Project documentation

✅ Task 1: Exploratory Data Analysis & Risk Metrics

Goal: Understand asset characteristics, correlations, and risk factors.

Key Analyses

Stationarity Test (ADF): Prices are non-stationary; returns are stationary

Volatility Analysis: TSLA shows high volatility, especially during 2020–2021

Correlation Analysis:

TSLA ↔ SPY: Moderate positive correlation (0.4–0.6)

BND ↔ Stocks: Very low correlation (0.0–0.2) → good diversification

Risk Metrics

Value at Risk (95%)

Conditional VaR

Sharpe Ratio

Maximum Drawdown

Insights

TSLA offers high return potential but introduces significant risk

BND provides stability and reduces portfolio volatility

SPY offers balanced risk-return profile

✅ Task 2: Model Selection & Evaluation (ARIMA)

Goal: Fit ARIMA models to TSLA prices and select the best one.

Models Compared
Model Order	AIC	RMSE	MAE
(0,1,0)	13646.47	77.96	62.97
(1,1,0)	13646.54	77.94	62.97
(0,1,1)	13646.59	77.94	62.97

Selected Model: ARIMA(0,1,0) (lowest AIC, simplest model)

Residual Analysis

High volatility during 2020–2021

Residuals are right-skewed with heavy tails

Q-Q plots show non-normal distribution → ARIMA struggles during extreme events

Conclusion: ARIMA captures overall trend but not volatility spikes → will use for baseline forecasts in Task 3.

✅ Task 3: LSTM Forecasting

Goal: Improve forecasting accuracy using deep learning.

LSTM Training Summary

Epochs: 25

Final validation loss: 0.0008

Model trained successfully with good convergence

Forecast Summary
Metric	Value
Current Price	$319.04
6-Month Forecast Price	$205.52
Price Change	-$113.52
Expected Return (6M)	-35.6%
Annualized Return	-71.2%

Confidence Interval:

Range: $205.52 – $301.93

Width: $96.41 (~30.2% of price)

Investment Recommendation

Defensive strategy → Reduce TSLA allocation to 5–10%

Increase BND allocation for stability

Focus on capital preservation

✅ Task 4: Portfolio Optimization

Goal: Allocate assets to minimize risk while considering forecasts.

Optimal Portfolios

1. Maximum Sharpe Ratio Portfolio

100% SPY, 0% TSLA, 0% BND

Return: 14.5%, Volatility: 18.2%, Sharpe: 0.547

2. Minimum Volatility Portfolio (Recommended)

TSLA: 0.0% | BND: 94.5% | SPY: 5.5%

Expected Return: 2.6%

Volatility: 5.4%

Sharpe Ratio: -0.343

Rationale: TSLA’s negative forecast (-71.2%) → prioritize capital preservation

✅ Task 5: Backtesting & Performance Evaluation

Goal: Validate the strategy against a 60/40 benchmark.

Performance Comparison
Metric	Strategy (Min Vol)	Benchmark (60/40)
Total Return	2.82%	12.92%
Annualized Return	2.87%	13.15%
Annualized Volatility	5.05%	12.28%
Sharpe Ratio	-0.3227	0.7039
Max Drawdown	-4.27%	-11.25%
Key Conclusions

✅ Lower volatility achieved

✅ Capital preservation focus succeeded



Final Verdict: Mixed results → strategy useful for risk-averse investors prioritizing stability.

🔍 Technical Workflow

Data Collection → yfinance

EDA & Risk Analysis → Task 1

Modeling

ARIMA (Task 2)

LSTM (Task 3)

Portfolio Optimization → Mean-Variance approach (Task 4)

Backtesting & Validation (Task 5)

⚙️ Git Workflow & CI/CD

Branching Strategy:

main → production-ready

dev → feature development

CI/CD: Implemented with GitHub Actions

Linting (flake8)

Notebook execution (nbconvert)

Unit testing (pytest)



🚀 How to Run the Project
# Clone repository
git clone https://github.com/ruhamds/Time_Series_Stock_Analysis.git
cd Time_Series_Stock_Analysis

# Install dependencies
pip install -r requirements.txt

# Run Jupyter notebooks
jupyter notebook

# Or execute main scripts
python src/portfolio_optimization.py