import yfinance as yf
import pandas as pd
from dash import html

def get_options_chain(ticker):
    try:
        stock = yf.Ticker(ticker)
        expirations = stock.options

        if not expirations:
            return html.P("No option expirations found.")

        next_expiry = expirations[0]  # Take the nearest expiry date
        calls = stock.option_chain(next_expiry).calls

        # Select relevant columns and clean up

        columns = ['strike', 'lastPrice', 'bid', 'ask', 'volume', 'openInterest']
        # calls = calls[columns].head(10)   ---no sorting by openInterest
        calls = calls[columns].sort_values(by='openInterest', ascending=False).head(10)


        # Build an HTML table for Dash
        return html.Table([
            html.Thead(html.Tr([html.Th(col) for col in calls.columns])),
            html.Tbody([
                html.Tr([html.Td(calls.iloc[i][col]) for col in calls.columns])
                for i in range(len(calls))
            ])
        ])
    except Exception as e:
        return html.P(f"Error fetching options: {str(e)}")
