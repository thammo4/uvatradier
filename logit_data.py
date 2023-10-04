from tradier import *

#
# Sample script that will fetch S&P 500 stocks and query the Tradier API to get OLHCV data
#

sp500 = pd.read_csv('https://raw.githubusercontent.com/datasets/s-and-p-500-companies/main/data/constituents.csv');

sp500_sample = sp500.sample(10);

sp500_symbols = list(sp500_sample['Symbol']);

df = pd.DataFrame({'symbol':[], 'profitable':[], 'volume_change':[]});

for s in sp500_symbols:
	bar_data = quotes.get_historical_quotes(s, interval='weekly', start_date='2023-08-01', end_date='2023-10-01');
	bar_data['profitable'] = (bar_data['close'] - bar_data['open'] > 0).astype(int);
	bar_data['volume_change'] = bar_data['volume'].diff();
	bar_data['symbol'] = s;
	df = df.append(bar_data[['symbol', 'profitable', 'volume_change']]);



#
# TO DO: BUILD LOGISTIC REGRESSION MODEL WITH df
#