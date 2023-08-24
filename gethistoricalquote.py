from config import *


def get_historical_quotes (symbol, interval='daily', start_date='', end_date=datetime.now().strftime('%Y-%m-%d')):
	'''
		This function returns a dataframe with historical bar data apropos the given symbol.
	'''

	if not start_date:
		start_date = (datetime.now()-timedelta(days=28)).strftime('%Y-%m-%d');

	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, HISTORICAL_ENDPOINT),
		params 	= {'symbol':symbol, 'interval':interval, 'start':start_date, 'end':end_date, 'session_filter':'all'},
		headers = REQUESTS_HEADERS
	);

	return pd.DataFrame(r.json()['history']['day']);