from config import *



def get_quote_day (symbol):
	'''
		This function fetches the current quote data about a given symbol
	'''

	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, QUOTES_ENDPOINT),
		params 	= {'symbols':symbol, 'greeks':'false'},
		headers = REQUESTS_HEADERS
	);

	return pd.json_normalize(r.json()['quotes']['quote']);