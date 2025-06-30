import yfinance as yf
import pandas as pd
from dash import html

def get_options_chain(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_price = stock.history(period='1d')['Close'].iloc[-1]

        expiry_dates = stock.options
        if not expiry_dates:
            return html.Div(f"No options data available for {ticker}")

        expiry = expiry_dates[0]  # Nearest expiry
        calls = stock.option_chain(expiry).calls

        # Filter: Out-of-the-money calls with decent liquidity
        filtered = calls[
            (calls['strike'] > stock_price) &
            (calls['openInterest'] > 100)
        ].copy()

        # Calculate projected income
        filtered['income'] = (filtered['bid'] * 100).round(2)

        # Pick top 10 by open interest
        filtered = filtered.sort_values(by='openInterest', ascending=False).head(10)

        # Columns to display
        columns = ['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest', 'income']
        column_tooltips = {
            'strike': 'Strike price (must be above current stock price)',
            'lastPrice': 'Last traded price of the option',
            'bid': 'Max buyer will pay',
            'ask': 'Min seller will accept',
            'volume': 'Contracts traded today',
            'openInterest': 'Open contracts (liquidity)',
            'income': 'Projected income from selling 1 call option (bid × 100)'
        }

        # Build the table
        header = html.Tr([
            html.Th(col, title=column_tooltips.get(col, "")) for col in columns
        ])
        body = html.Tbody([
            html.Tr([
                html.Td(filtered.iloc[i][col]) for col in columns
            ]) for i in range(len(filtered))
        ])
        return html.Table([html.Thead(header), body])

    except Exception as e:
        return html.Div(f"Error fetching options: {e}")
