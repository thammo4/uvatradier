from config import *

#
# Helper function used to index the start of the trading week
#

def last_monday (input_date):
	'''
	Find the date of the previous Monday for a given input date.

	Args:
		input_date (datetime.date): the input date

	Returns:
		datetime.date: The date of the previous Monday.
	'''

	return (input_date - timedelta(days=(input_date.weekday())));


#
# Fetch historical stock data
#

def get_historical_quotes (symbol, interval='daily', start_date=False, end_date=False):
	'''
	Fetch historical stock data for a given symbol within a specified date range.

	Args:
		symbol (str): 				The stock ticker symbol.

		interval (str, optional) 	The interval of data. Default is 'daily'. Alt values are weekly and monthly.

		start_date (str, optional) 	The start of the date range in 'YYYY-MM-DD' format.
			If not provided, the function sets the start_date to be the Monday preceding the end_date.

		end_date (str, optional) 	The end of the date range in 'YYYY-MM-DD' format.
			If not provided, the end_date is set to be the current date.

	Returns:
		pandas.DataFrame: A DataFrame with columns: [date, open, high, low, close, volume]

	Note:
		This function requires that global constants SANDBOX_URL, QUOTES_HISTORICAL_ENDPOINT, and REQUESTS_HEADERS be defined in config.

	Example:
		get_historical_quotes (symbol='MMM', interval='daily', start_date='2023-06-01', end_date='2023-06-12')
	'''

	if not end_date:
		end_date = datetime.today().strftime('%Y-%m-%d');

	if not start_date:
		tmp = datetime.strptime(end_date, '%Y-%m-%d');
		start_date = last_monday(tmp).strftime('%Y-%m-%d');

	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, QUOTES_HISTORICAL_ENDPOINT),
		params 	= {
			'symbol' 	: symbol,
			'interval' 	: interval,
			'start' 	: start_date,
			'end' 		: end_date
		},
		headers = REQUESTS_HEADERS
	);

	return pd.DataFrame(r.json()['history']['day']);

