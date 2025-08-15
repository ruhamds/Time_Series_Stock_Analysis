# Time Series Stock Analysis Project 📈

This project focuses on analyzing historical financial data, forecasting stock prices, and constructing an optimized investment portfolio using statistical (ARIMA) and machine learning (LSTM) models. The analysis spans three key assets: **TSLA (Tesla Inc.)**, **BND (Vanguard Total Bond Market ETF)**, and **SPY (S&P 500 ETF)** over a 10-year period (July 1, 2015 – July 31, 2025).

## 📌 Project Overview

The project is divided into five tasks:
1. **Task 1: Exploratory Data Analysis & Risk Assessment**  
   - Understand asset characteristics, correlations, and risk factors.
2. **Task 2: Model Selection & Evaluation (ARIMA)**  
   - Fit and evaluate ARIMA models for baseline forecasting.
3. **Task 3: Advanced Forecasting with LSTM**  
   - Leverage deep learning for improved price predictions.
4. **Task 4: Portfolio Optimization**  
   - Optimize asset allocation using forecast insights.
5. **Task 5: Backtesting & Performance Evaluation**  
   - Validate the strategy against a benchmark.

## 📂 Project Structure
Time_Series_Stock_Analysis/
├── Notebooks/
│   ├── Task1/          # EDA & risk analysis (e.g., stationarity, volatility)
│   ├── Task2/          # ARIMA modeling (e.g., model selection, residuals)
│   ├── Task3/          # LSTM forecasting (e.g., training, forecast visuals)
│   ├── Task4/          # Portfolio optimization (e.g., Sharpe ratio portfolios)
│   └── Task5/          # Backtesting & performance (e.g., metrics comparison)
├── src/
│   ├── data_definition.py    # Data loading and preprocessing
│   ├── forecast_analysis.py  # Forecasting logic (ARIMA, LSTM)
│   ├── forecast_visualize.py # Visualization functions
│   ├── portfolio_optimization.py  # Optimization algorithms
│   └── portfolio_optimization_prep.py  # Prep data for optimization
├── .github/
│   └── workflows/
│       └── ci.yml           # CI pipeline for linting and testing
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation

### Task 1: Exploratory Data Analysis & Risk Metrics
- **Goal:** Assess asset behavior and risk.
- **Key Analyses:**
  - **Stationarity Test (ADF):** Prices non-stationary; returns stationary.
  - **Volatility Analysis:** TSLA highly volatile (2020–2021 spike).
  - **Correlation Analysis:**
    - TSLA ↔ SPY: Moderate positive (0.4–0.6).
    - BND ↔ Stocks: Low (0.0–0.2) → diversification benefit.
- **Risk Metrics:**
  - Value at Risk (95%)
  - Conditional VaR
  - Sharpe Ratio
  - Maximum Drawdown
- **Insights:** TSLA offers high returns but significant risk; BND stabilizes; SPY balances risk-return.

### Task 2: Model Selection & Evaluation (ARIMA)
- **Goal:** Fit ARIMA to TSLA and select the best model.
- **Models Compared:**
  | Model  | AIC      | RMSE  | MAE  |
  |--------|----------|-------|------|
  | (0,1,0)| 13646.47 | 77.96 | 62.97|
  | (1,1,0)| 13646.54 | 77.94 | 62.97|
  | (0,1,1)| 13646.59 | 77.94 | 62.97|
- **Selected Model:** ARIMA(0,1,0) (lowest AIC, simplest).
- **Residual Analysis:** High volatility (2020–2021), right-skewed residuals, non-normal Q-Q plots.
- **Conclusion:** ARIMA captures trends but struggles with volatility spikes; serves as baseline for Task 3.

### Task 3: LSTM Forecasting
- **Goal:** Enhance forecasting with deep learning.
- **LSTM Training:**
  - Epochs: 25
  - Final validation loss: 0.0008
- **Forecast Summary:**
  | Metric              | Value       |
  |---------------------|-------------|
  | Current Price       | $319.04     |
  | 6-Month Forecast    | $205.52     |
  | Price Change        | -$113.52    |
  | Expected Return (6M)| -35.6%      |
  | Annualized Return   | -71.2%      |
- **Confidence Interval:** $205.52 – $301.93 (Width: $96.41, ~30.2%).
- **Recommendation:** Defensive strategy—reduce TSLA to 5–10%, increase BND for stability.

### Task 4: Portfolio Optimization
- **Goal:** Minimize risk with forecast insights.
- **Optimal Portfolios:**
  - **Max Sharpe Ratio:**
    - 100% SPY, 0% TSLA, 0% BND
    - Return: 14.5%, Volatility: 18.2%, Sharpe: 0.547
  - **Min Volatility (Recommended):**
    - TSLA: 0.0%, BND: 94.5%, SPY: 5.5%
    - Return: 2.6%, Volatility: 5.4%, Sharpe: -0.343
- **Rationale:** TSLA’s negative forecast (-71.2%) prioritizes capital preservation.

### Task 5: Backtesting & Performance Evaluation
- **Goal:** Validate strategy vs. 60/40 benchmark.
- **Performance Comparison:**
  | Metric            | Min Vol Strategy | 60/40 Benchmark |
  |-------------------|------------------|-----------------|
  | Total Return      | 2.82%            | 12.92%          |
  | Annualized Return | 2.87%            | 13.15%          |
  | Volatility        | 5.05%            | 12.28%          |
  | Sharpe Ratio      | -0.3227          | 0.7039          |
  | Max Drawdown      | -4.27%           | -11.25%         |
- **Conclusions:** Lower volatility achieved; capital preservation succeeded. Mixed results—best for risk-averse investors.

## 🔍 Technical Workflow
- **Data Collection:** `yfinance`
- **EDA & Risk Analysis:** Task 1
- **Modeling:**
  - ARIMA (Task 2)
  - LSTM (Task 3)
- **Portfolio Optimization:** Mean-Variance approach (Task 4)
- **Backtesting & Validation:** Task 5

## ⚙️ Git Workflow & CI/CD
- **Branching Strategy:**
  - `main`: Production-ready
  - `dev`: Feature development
- **CI/CD (GitHub Actions):**
  - Linting (`flake8`)
  - Notebook execution (`nbconvert`)
  - Unit testing (`pytest`)

## 🚀 How to Run the Project
1. **Clone the repository:**
   ```bash
   git clone https://github.com/ruhamds/Time_Series_Stock_Analysis.git
   cd Time_Series_Stock_Analysis

Install dependencies:
bashpip install -r requirements.txt

Run Jupyter notebooks:
bashjupyter notebook

Execute main scripts:
bashpython src/portfolio_optimization.py


📝 About
This project demonstrates a comprehensive time series analysis pipeline for stock market data, blending traditional and modern forecasting techniques with portfolio management.
🌟 Contributions

Fork the repository and submit pull requests.
Report issues or suggest enhancements via GitHub Issues.

📊 Resources

Project Repository
yfinance Documentation




