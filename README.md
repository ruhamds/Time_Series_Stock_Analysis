# Time Series Analysis Project

This project demonstrates how to perform time series analysis and stationarity checks using the Augmented Dickey-Fuller (ADF) test, as well as applying first-order differencing to achieve stationarity.

---

## 📂 Project Structure

project/
│
├── data/ # Contains raw and processed datasets (.csv)
├── results/ # Stores output figures, plots, and results
├── scripts/ # Python scripts for analysis
├── .gitignore # Ignore unnecessary files
├── README.md # Project documentation
└── requirements.txt # Python dependencies


---

## 🚀 Getting Started

### 1️⃣ Clone the repository

git clone https://github.com/ruhamds/Time_Series_Stock_Analysis.git
cd your-repo-name

2️⃣ Create a virtual environment

python -m venv venv
source venv/bin/activate   # On Mac/Linux
venv\Scripts\activate      # On Windows

3️⃣ Install dependencies

pip install -r requirements.txt

📊 How to Run the Analysis
Run the following command:

python scripts/adf_test.py
This will:

Load the dataset from the data/ folder.

Perform the ADF test on the original series.

Apply first-order differencing.

Perform the ADF test again to check for stationarity.

📁 .gitignore
The .gitignore file is set to exclude:

*.pkl
*.csv
results/
🧪 Example Output

ADF Statistic (Original): -0.9453
p-value (Original): 0.7723
Interpretation: The original series is Non-Stationary.

ADF Statistic (Differenced): -12.3456
p-value (Differenced): 0.0000
Interpretation: The differenced series is Stationary.

📌 Requirements
Python 3.8+

pandas

numpy

statsmodels

matplotlib










