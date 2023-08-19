"""
extracting data using alpha vantage

"""

# importing libraries
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

api_key = # Generate your own API Key

# extracting data for a single ticker
ts = TimeSeries(key = api_key, output_format = 'pandas')
data = ts.get_intraday(symbol = 'MSFT', outputsize = 'full')[0]
data.columns = ["open", "high", "low", "close", "volume"]
data = data.iloc[::-1]


# extracting stock data (historical close price) for multiple stocks
all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "GOOGL", "META"]
close_prices = pd.DataFrame()
api_call_count = 1
ts = TimeSeries(key = api_key, output_format = 'pandas')
start_time = time.time()
for ticker in all_tickers:
  data = ts.get_intraday(symbol = ticker, interval = '5min', outputsize = 'compact')[0]
  api_call_count += 1
  data.columns = ["open", "high", "low", "close", "volume"]
  data = data.iloc[::-1]
  close_prices[ticker] = data["close"]
  if api_call_count == 5:
    api_call_count = 1
    time.sleep(60 - ((time.time() - start_time) % 60.0))


# extracting ohlcv data for multiple stocks
all_tickers = ["AAPL", "MSFT", "CSCO", "AMZN", "GOOGL", "META"]
ohlv_dict = {}
api_call_count = 1
ts = TimeSeries(key = api_key, output_format = 'pandas')
start_time = time.time()
for ticker in all_tickers:
    data = ts.get_intraday(symbol = ticker, interval = '1min', outputsize = 'compact')[0]
    api_call_count += 1
    data.columns = ["open", "high", "low", "close", "volume"]
    data = data.iloc[::-1]
    ohlv_dict[ticker] = data
    if api_call_count == 5:
        api_call_count = 1
        time.sleep(60 - ((time.time() - start_time) % 60.0))