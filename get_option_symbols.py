from config import *




def get_option_symbols (underlying_symbol):
	'''
		This function provides a convenient wrapper to fetch option symbols
		for a specified underlying_symbol
	'''
	r = requests.get(
		url 		= '{}/{}'.format(SANDBOX_URL, OPTION_SYMBOL_ENDPOINT),
		params 		= {'underlying':underlying_symbol},
		headers 	= REQUESTS_HEADERS
	);
	return r.json()['symbols'][0]['options'];