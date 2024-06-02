import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf

# Define the file paths to save/load the data
EURUSD_PATH = 'EURUSD_data.csv'
AUDUSD_PATH = 'AUDUSD_data.csv'

def download_data(filepath, ticker_symbol):
    """Download currency data or load from a file, handling missing data."""
    if os.path.exists(filepath):
        data = pd.read_csv(filepath, index_col='Date', parse_dates=True)
        print(f"Data for {ticker_symbol} loaded from disk.")
    else:
        data = yf.download(ticker_symbol, start="2000-01-01", interval='1d')

        if data.empty:
            print(f"Failed to download data for {ticker_symbol}. Exiting.")
            exit()
        data.dropna(inplace=True)  # Remove rows with NaN values
        data.to_csv(filepath)
        print(f"Data for {ticker_symbol} downloaded, cleaned, and saved to disk.")
    return data

def calculate_ema(data, span=200):
    """Calculate Exponential Moving Average."""
    return data['Close'].ewm(span=span, adjust=False).mean()

def plot_data(data):
    """Plot the Close price and EMA of the data."""
    plt.figure(figsize=(14, 7))
    plt.plot(data['Close'], label='Close Price')
    plt.plot(data['200 EMA'], label='200-day EMA', color='orange')
    plt.title('Close Price and 200-day EMA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid(True)
    plt.show()

def calculate_returns(data):
    """Calculate the daily returns."""
    return data['Close'].pct_change(1)

def plot_covariance_matrix(eurusd_returns, audusd_returns):
    """Plot covariance matrix between EURUSD and AUDUSD returns."""
    df = pd.DataFrame({
        'EURUSD Returns': eurusd_returns,
        'AUDUSD Returns': audusd_returns
    }).dropna()
    covariance_matrix = df.cov()
    sns.heatmap(covariance_matrix, annot=True, cmap='coolwarm')
    plt.title('Covariance matrix between EURUSD and AUDUSD Returns')
    plt.show()
# Main usage
if __name__ == "__main__":
    eurusd_data = download_data(EURUSD_PATH, 'EURUSD=X')
    audusd_data = download_data(AUDUSD_PATH, 'AUDUSD=X')
    eurusd_data['200 EMA'] = calculate_ema(eurusd_data, 200)
    audusd_data['200 EMA'] = calculate_ema(audusd_data, 200)

    eurusd_returns = calculate_returns(eurusd_data)
    audusd_returns = calculate_returns(audusd_data)

    plot_covariance_matrix(eurusd_returns, audusd_returns)
