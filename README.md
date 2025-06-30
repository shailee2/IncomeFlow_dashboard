# IncomeFlow Dashboard

A real-time, interactive dashboard to explore stock prices and options chain data for income-focused strategies like **covered calls** and **cash-secured puts**. Built with Dash, Plotly, and yFinance, this tool helps retail investors simulate the screening logic used by trading desks.

## Features

- Real-time stock price charts for user-defined tickers  
- Options chain table with filters for open interest and bid-ask spread  
- Premium income projections based on current bid prices  
- Highlighting of favorable trades (e.g., high-liquidity covered calls)  
- Built-in logic for risk profiles like **cash-secured puts**

## Tech Stack

- Python, Dash, Plotly, yFinance, pandas  
- Modular architecture with `app.py` and `options_data.py`  
- REST-style data flow with clear state separation and real-time updates

## Project Structure

Mag7_dashboard/

├── app.py                   # Main Dash app logic <br>
├── options_data.py          # Modular logic for fetching/formatting options data <br>
├── assets/                  # Optional CSS or static assets <br>
└── backup/                  # Saved snapshots or experiment files <br>

## Run Locally

### 1. Clone the repository
```
git clone https://github.com/shailee2/IncomeFlow_dashboard.git
cd IncomeFlow_dashboard
```
### 2. Install dependencies
```
pip install -r requirements.txt
```
### 3. Run the app
``` 
python app.py

# Visit http://127.0.0.1:8050 in your browser
```

##  Future Enhancements
- Add implied volatility and delta filters via a paid API
- Portfolio-level income simulation
- Weekly performance snapshots
