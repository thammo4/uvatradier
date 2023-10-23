from config import *

def married_put (symbol, equity_quantity, option_symbol, option_quantity, duration='day'):
	'''
		Married put is a bullish strategy that seeks to limit losses in the event that the underlying asset has an
		unexpected decrease in price. It involves the following components:
			• long asset
			• long ATM put on asset

		Arguments:
			symbol: underlying asset
			equity_quantity: number of shares of underlying to long
			option_symbol: OCC option contract symbol
			option_quantity: number of option contracts to purchase
			duration: day, gtc, pre, post

		Returns:
			json from HTTP post request to indicate success

	'''
	r = requests.post(
		url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		data 	= {
			'class' 			: 'combo',
			'symbol' 			: symbol,
			'type' 				: 'market',
			'duration' 			: duration,
			'side[0]' 			: 'buy',
			'quantity[0]' 		: equity_quantity,
			'option_symbol[1]' 	: option_symbol,
			'side[1]' 			: 'buy_to_open',
			'quantity[1]' 		: option_quantity
		},
		headers = REQUESTS_HEADERS
	);

	return r.json();