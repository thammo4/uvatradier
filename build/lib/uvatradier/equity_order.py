from .base import Tradier

import requests
import pandas as pd


class EquityOrder (Tradier):
	def __init__ (self, account_number, auth_token):
		Tradier.__init__(self, account_number, auth_token);

		#
		# Order endpoint
		#

		self.ORDER_ENDPOINT = "v1/accounts/{}/orders".format(self.ACCOUNT_NUMBER); # POST

	def order (self, symbol, side, quantity, order_type, duration='day', limit_price=False, stop_price=False):
		'''
			Arguments:
				symbol 		= Stock Ticker Symbol.
				side 		= ['buy', 'buy_to_cover', 'sell', 'sell_short']
				order_type 	= ['market', 'limit', 'stop', 'stop_limit']
				duration 	= ['day', 'gtc', 'pre', 'post']

			Example of how to run:
				>>> eo = EquityOrder(ACCOUNT_NUMBER, AUTH_TOKEN)
				>>> eo.order(symbol='QQQ', side='buy', quantity=10, order_type='market', duration='gtc');
				{'order': {'id': 8256590, 'status': 'ok', 'partner_id': '3a8bbee1-5184-4ffe-8a0c-294fbad1aee9'}}
		'''

		#
		# Define initial requests parameters dictionary whose fields are applicable to all order_type values
		#

		r_params = {
			'class'  	: 'equity',
			'symbol' 	: symbol,
			'side' 		: side,
			'quantity' 	: quantity,
			'type' 		: order_type,
			'duration' 	: duration
		};

		#
		# If the order_type is limit, stop, or stop_limit --> Set the appropriate limit price or stop price
		#

		if order_type.lower() in ['limit', 'stop_limit']:
			r_params['price'] = limit_price;
		if order_type.lower() in ['stop', 'stop_limit']:
			r_params['stop'] = stop_price;

		r = requests.post(
			url = '{}/{}'.format(self.BASE_URL, self.ORDER_ENDPOINT),
			params = r_params,
			headers=self.REQUESTS_HEADERS
		);

		return r.json();