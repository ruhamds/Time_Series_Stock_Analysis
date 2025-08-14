📈 Tesla & Portfolio Optimization Project
Overview

This project applies exploratory data analysis, performance metrics evaluation, LSTM-based forecasting, and portfolio optimization to build a model-driven investment strategy.
Our main case study focuses on Tesla (TSLA), incorporating S&P 500 (SPY) and US Bond Index (BND) for diversification.

The project is structured into 5 tasks, each producing key insights for final investment recommendations.

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
├── requirements.txt # Python dependencies
└── README.md        # Project documentation


Task 1: Exploratory Data Analysis (EDA)

We explored historical stock data for TSLA, SPY, and BND:

Checked for missing values, outliers, and data consistency

Visualized daily closing prices, returns, and volatility trends

Observed TSLA's higher volatility compared to SPY & BND

Key EDA Insights:

TSLA’s price swings are significantly larger than SPY & BND

Bonds (BND) exhibit stable, low-volatility patterns

TSLA’s price cycles are tied to macroeconomic events & earnings announcements

Task 2: Performance Metrics Analysis

We calculated risk & return metrics:

Annualized Return

Volatility

Sharpe Ratio

Max Drawdown

Value at Risk (VaR)

Example TSLA Metrics:

Metric	Value
Annual Return	23.1%
Volatility	55.2%
Sharpe Ratio	0.42
Max Drawdown	-73.4%
Task 3: Forecasting & Portfolio Optimization

Using an LSTM model:

TSLA forecast: -71.2% expected return (negative outlook)

Optimization prioritized minimum volatility portfolio over return maximization

Task 4: Final Portfolio Recommendation

Optimal Portfolio Allocation:

Asset	Allocation
TSLA	0.0%
BND	94.5%
SPY	5.5%

Portfolio Metrics:

Expected Annual Return: 2.6%

Annual Volatility: 5.4%

Sharpe Ratio: -0.343

95% VaR (daily): -0.549%

Rationale:

Avoided TSLA exposure due to negative forecast

Focused on capital preservation with heavy bond allocation

Accepted lower returns for controlled risk

Task 5: Backtest Results

Performance Summary:

Strategy Return: 2.82%

Benchmark Return (SPY): 12.92%

Sharpe Ratio: Strategy -0.323, Benchmark 0.704

Risk Analysis:

Volatility: Strategy 5.0%, Benchmark 12.3%

Max Drawdown: Strategy -4.3%, Benchmark -11.2%

52% of trading days were positive

Conclusion:

Strategy underperformed in returns but succeeded in risk reduction

Forecast-based portfolio avoided major losses from TSLA

Trade-off between stability and missed growth opportunities

📌 Final Verdict

This project demonstrates:

Data-driven investment decisions using EDA, risk metrics, and forecasts

Portfolio optimization that aligns with investor risk tolerance

The importance of backtesting before real-world application

🚀 How to Run

Clone the repository:

git clone https://github.com/ruhamds/Time_Series_Stock_Analysis.git


Install dependencies:

pip install -r requirements.txt


Open Jupyter Notebooks in task1/–task5/ and run sequentially.

📊 Tech Stack

Python (pandas, numpy, matplotlib, seaborn)

Finance: yfinance, PyPortfolioOpt

ML: TensorFlow/Keras (LSTM)

Optimization: Mean-Variance, Sharpe Ratio maximization

Risk Analysis: VaR, Drawdown

