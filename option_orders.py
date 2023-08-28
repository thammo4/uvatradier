from config import *




#
# Bull-call spread
#

def bull_call_spread (underlying_symbol, option_symbol_0, quantity_0, option_symbol_1, quantity_1, duration='day'):
	r = requests.post(
		url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		data 	= {
			'class' 			: 'multileg',
			'symbol' 			: underlying_symbol,
			'type' 				: 'market',
			'duration' 			: duration,
			'option_symbol[0]' 	: option_symbol_0,
			'side[0]' 			: 'buy_to_open',
			'quantity[0]' 		: quantity_0,
			'option_symbol[1]' 	: option_symbol_1,
			'side[1]' 			: 'sell_to_open',
			'quantity[1]' 		: quantity_1
		},
		headers = REQUESTS_HEADERS
	);

	return r.json();







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