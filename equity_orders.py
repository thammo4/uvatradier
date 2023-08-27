from config import *


#
# Post data for equity market order
#

def equity_market_order (symbol, side, quantity, duration='day'):
	'''
		This function will place a simple market order for the supplied symbol.
		By default, the order is good for the day. Per the nature of market orders, it should be filled.

		Parameter Notes:
			side 		= buy, buy_to_cover, sell, sell_short
			duration 	= day, gtc, pre, post
	'''

	r = requests.post(
		url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		params 	= {
			'class'		: 'equity',
			'symbol' 	: symbol,
			'side' 		: side,
			'quantity' 	: quantity,
			'type' 		: 'market',
			'duration' 	: duration
		},
		headers = REQUESTS_HEADERS
	);

	return r.json();


#
# Post data for equity limit order
#

def equity_limit_order (symbol, side, quantity, limit_price, duration='day'):
	'''
		This function places a limit order to buy/sell the given symbol at the specified limit_price (or better).
		Recall that a limit order guarantees the execution price. However, the order might not execute at all.

		Parameter Notes:
			side 		= buy, buy_to_cover, sell, sell_short
			duration 	= day, gtc, pre, post
	'''
	r = requests.post(
		url = '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		data = {
			'class' 	: 'equity',
			'symbol' 	: symbol,
			'side' 		: side,
			'quantity' 	: quantity,
			'type' 		: 'limit',
			'duration' 	: duration,
			'price' 	: limit_price
		},
		headers = REQUESTS_HEADERS
	);

	return r.json();