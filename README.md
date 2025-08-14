📈 Time Series Stock Analysis & Portfolio Optimization

This project is an end-to-end financial data analysis and forecasting pipeline focused on Tesla stock and a multi-asset portfolio. It combines time series forecasting, model evaluation, and portfolio optimization to provide insights into market trends, investment strategies, and potential risks.

🚀 Features

Data Exploration & Preprocessing (Task 1)

Time Series Forecasting Model Development (Task 2)

Tesla Stock Price Forecasting (Task 3)

Portfolio Optimization using Modern Portfolio Theory (Task 4)

Portfolio Impact Analysis for forecasted changes (Task 5)

Visualization of Forecasts & Optimization Results

📂 Project Structure
.
├── Notebooks/
│   ├── Task1/                       # Data collection & EDA
│   ├── Task2/                       # Model building & evaluation
│   ├── Task3/                       # Tesla forecast generation & analysis
│   ├── Tak4/                        # Portfolio optimization
│   ├── Task5/                       # Portfolio impact analysis
│  
│
├── src/
│   ├── data_definition.py           # Defines data structures and constants
│   ├── forecast_analysis.py         # Forecast evaluation & metrics
│   ├── forecast_visualize.py        # Visualization utilities for forecasts
│   ├── portfolio_optimization.py    # Core portfolio optimization logic
│   ├── portfolio_optimization_prep.py # Data prep for optimization
│
├── task4_optimization_template.py   # Template for optimization experiments
└── README.md

📊 Tasks Breakdown
Task 1 – Data Collection & EDA

Gathered Tesla stock data (and other assets for portfolio analysis).

Cleaned and structured the dataset for analysis.

Performed exploratory analysis:

Historical price trends.

Seasonal patterns & volatility.

Volume & return distribution.

Task 2 – Model Development

Built and compared multiple time series models:

ARIMA

SARIMA

LSTM (deep learning)

Evaluated using metrics like RMSE, MAE, MAPE.

Selected best-performing model for forecasting.

Task 3 – Tesla Price Forecast

Generated 6–12 month forecasts using the chosen model.

Plotted forecasts with confidence intervals.

Analyzed:

Trend direction.

Confidence interval changes over time.

Potential market opportunities & risks.

Task 4 – Portfolio Optimization

Built a portfolio with Tesla + other assets.

Used Modern Portfolio Theory to:

Calculate optimal asset weights.

Maximize returns for given risk.

Visualize the Efficient Frontier.

Task 5 – Portfolio Impact Analysis

Integrated forecasted Tesla returns into portfolio simulation.

Analyzed potential portfolio performance changes.

Identified diversification benefits & risk exposure.



⚙️ Installation & Usage
# Clone the repository
git clone https://github.com/ruhamds/time_series_stock_analysis.git
cd time_series_stock_analysis

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run example usage
python example_usage.py

📌 Requirements

Python 3.9+

pandas, numpy, matplotlib, seaborn

statsmodels, scikit-learn

keras/tensorflow (for LSTM)

yfinance (for data retrieval)

📑 License

This project is licensed under the MIT License.

