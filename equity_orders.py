from config import *


def equity_market_order (symbol, side, quantity, duration='day'):
	'''
		This function will place a simple market order for the supplied symbol.
		By default, the order is good for the day. Per the nature of market orders, it should be filled.
	'''

	r = requests.post(
		url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		params 	= {'class':'equity', 'symbol':symbol, 'side':side, 'quantity':quantity, 'type':'market', 'duration':duration},
		headers = REQUESTS_HEADERS
	);

	return r.json();