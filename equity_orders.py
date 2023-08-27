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




#
# Post data for equity stop-loss or stop-entry orders
#

def equity_stop_order (symbol, side, quantity, stop_price, duration='day'):
	'''
		This function places a stop-loss or stop-entry order to buy/sell equities.
		Recall that a stop order will trigger in the direction of the stock's movement

		Parameter Notes:
			side 		= buy, buy_to_cover, sell, sell_short
			duration 	= day, gtc, pre, post
	'''

	r = requests.post(
		url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		data 	= {
			'class' 	: 'equity',
			'symbol' 	: symbol,
			'side' 		: side,
			'quantity' 	: quantity,
			'type' 		: 'stop',
			'duration' 	: duration,
			'stop' 		: stop_price
		},
		headers = REQUESTS_HEADERS
	);

	return r.json();





#
# Post data for equity stop-limit order
#

def equity_stop_limit_order (symbol, side, quantity, stop_price, limit_price, duration='day'):
	'''
		This function places a stop limit order with user-specified stop and limit prices.
		Recall that the stop_price indicates the price at which the order will convert into a limit order.
		(This contrasts an ordinary stop order, which will convert into a market order at the stop price.)

		The limit_price indicates the limit price once the order becomes a limit order.

		Buy stop limit orders are placed with a price in excess of the current stock price.
		Sell stop limit orders are placed below the current stock price.

		Parameter Notes:
			stop_price 	= stop price
			limit_price	= limit price
			side 		= buy, buy_to_cover, sell, sell_short
			duration 	= day, gtc, pre, post

	'''
	r = requests.post(
		url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		data 	= {
			'class' 	: 'equity',
			'symbol' 	: symbol,
			'side' 		: side,
			'quantity' 	: quantity,
			'type' 		: 'stop_limit',
			'duration' 	: duration,
			'price' 	: limit_price,
			'stop' 		: stop_price
		},
		headers = REQUESTS_HEADERS
	);

	return r.json();