from config import *


#
# Order contract market order
#

def option_market_order (underlying_symbol, option_symbol, side, quantity, duration='day'):
	'''
		This function places a simple market order to long/short an option contract.
		Valid argument values:
			side 		= buy_to_open, buy_to_close, sell_to_open, sell_to_close
			duration 	= day, gtc, pre, post
	'''
	r = requests.post(
		url = '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		data = {
			'class' 		: 'option',
			'symbol' 		: underlying_symbol,
			'option_symbol' : option_symbol,
			'side' 			: side,
			'quantity' 		: quantity,
			'type' 			: 'market',
			'duration' 		: duration
		},
		headers = REQUESTS_HEADERS
	);

	print(r.json());