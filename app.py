import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

from options_data import get_options_chain


# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Mag7 Options & Stock Dashboard"

# Define the list of stocks to choose from
stocks = ['AAPL', 'MSFT', 'NVDA']

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Mag7 Stock Dashboard"),

    dcc.Dropdown(
        id='stock-selector',
        options=[{'label': s, 'value': s} for s in stocks],
        value='AAPL'  # default
    ),

    dcc.Graph(id='stock-price-chart'),

    html.H3("Covered Call Candidates (Next Expiry - OTM Calls with High Open Interest)"),

    # ✅ This should be html.Div, not dcc.Graph
    html.Div(id='options-table')

])

# Callback: When the dropdown changes, update the graph
@app.callback(
    Output('stock-price-chart', 'figure'),
    Input('stock-selector', 'value')
)

def update_price_chart(ticker):
    if ticker is None:
        return go.Figure().update_layout(title='No ticker selected')

    end = datetime.now().date()
    start = end - timedelta(days=45)

    df = yf.download(ticker, start=start, end=end, interval='1d', progress=False, threads=False)
    print(f"Downloaded {len(df)} rows for {ticker}")

    # Flatten columns if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df = df.tail(30)
    df.index = pd.to_datetime(df.index)
    df['Close'] = df['Close'].round(2)

    if df.empty or 'Close' not in df.columns:
        return go.Figure().update_layout(title='No data available')

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines+markers', name=ticker))
    fig.update_layout(title=f'{ticker} Price - Last 30 Days',
                      xaxis_title='Date', yaxis_title='Close Price')
    return fig

@app.callback(
    Output('options-table', 'children'),
    Input('stock-selector', 'value')
)


def update_options_table(ticker):
    return get_options_chain(ticker)


# Run the app
if __name__ == '__main__':
   # app.run_server(debug=True)
    app.run(debug=True)
