from tradier import *

import yfinance as yf;


#
# Fetch OLHCV bar data for Conoco-Phillips
#

ticker = yf.Ticker('COP');
ticker_data = ticker.history(period='1d', start='2023-09-01', end='2023-10-01');

print(ticker_data);