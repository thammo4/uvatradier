from config import *

def get_quote_day (symbol, last_price=False):
	'''
		This function fetches the current quote data about a given symbol

		Example Usage:
			Fetch the last price of a given stock: last_price = get_quote_day('VMC', last_price=True)
	'''

	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, QUOTES_ENDPOINT),
		params 	= {'symbols':symbol, 'greeks':'false'},
		headers = REQUESTS_HEADERS
	);

	df_quote = pd.json_normalize(r.json()['quotes']['quote']);

	if last_price:
		return float(df_quote['last']);

	return df_quote;