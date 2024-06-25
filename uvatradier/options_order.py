from .base import Tradier

import requests
import pandas as pd
import re

class OptionsOrder (Tradier):
	def __init__ (self, account_number, auth_token, live_trade=False):
		Tradier.__init__(self, account_number, auth_token, live_trade);

		#
		# Order endpoint
		#

		self.ORDER_ENDPOINT = "v1/accounts/{}/orders".format(account_number); # POST


	#
	# Bear-put spread
	#

	def bear_put_spread (self, underlying, option0, quantity0, option1, quantity1, duration='day'):
		'''
			Parameters
				underlying: asset symbol (e.g. 'SPY')
				option0: OCC symbol of
		'''
		r = requests.post(
			url 	= '{}/{}'.format(self.BASE_URL, self.ORDER_ENDPOINT),
			data 	= {
				'class' 			: 'multileg',
				'symbol' 			: underlying,
				'type' 				: 'market',
				'duration' 			: duration,
				'option_symbol[0]' 	: option0,
				'side[0]' 			: 'buy_to_open',
				'quantity[0]' 		: quantity0,
				'option_symbol[1]' 	: option1,
				'side[1]' 			: 'sell_to_open',
				'quantity[1]' 		: quantity1
			},
			headers = self.REQUESTS_HEADERS
		);

		return r.json();


	#
	# Bear-call spread
	#

	def bear_call_spread (self, underlying, option0, quantity0, option1, quantity1, duration='day'):
		'''
			Bear call spread example:
				• XYZ @ $50/share
				• Pr(XYZ < $55/share) > .50
				• Legs
					• Short Call with K1 ≥ S (e.g. K1=55 > S=50) and receive $3 premium
					• Long Call with K2 > K1 ≥ S (e.g. K2=60 > K1=55 ≥ S=50) and pay $1 premium
				• Expiry t=T
					• If S(T) < K1 -> payoff = premium differential
					• If K1 < S(T) < K2
						• short call exercised and must sell at K1 = $55
						• long call expires OTM
						• payoff = (K1-K2) + (premium differential) < 0
					• If S(T) > K2 > K1
						• short call exercised and must sell at K1 = $55
						• long call exercised and can buy XYZ at K2 = $60
						• payoff = (K1-K2) + (premium differential) < 0
		'''
		r = requests.post(
			url 	= '{}/{}'.format(self.BASE_URL, self.ORDER_ENDPOINT),
			data 	= {
				'class' 			: 'multileg',
				'symbol' 			: underlying,
				'type' 				: 'market',
				'duration' 			: duration,
				'option_symbol[0]' 	: option0,
				'side[0]' 			: 'buy_to_open',
				'quantity[0]' 		: quantity0,
				'option_symbol[1]' 	: option1,
				'side[1]' 			: 'sell_to_open',
				'quantity[1]' 		: quantity1
			},
			headers = self.REQUESTS_HEADERS
		);

		return r.json();



	#
	# Bull-put spread
	#

	def bull_put_spread (self, underlying_symbol, option_symbol_0, quantity_0, option_symbol_1, quantity_1, duration='day'):
		r = requests.post(
			url 	= '{}/{}'.format(self.BASE_URL, self.ORDER_ENDPOINT),
			data 	= {
				'class' 			: 'multileg',
				'symbol' 			: underlying_symbol,
				'type' 				: 'market',
				'duration' 			: duration,
				'option_symbol[0]' 	: option_symbol_0,
				'side[0]' 			: 'sell_to_open',
				'quantity[0]' 		: quantity_0,
				'option_symbol[1]' 	: option_symbol_1,
				'side[1]' 			: 'buy_to_open',
				'quantity[1]' 		: quantity_1
			},
			headers = self.REQUESTS_HEADERS
		);

		return r.json();

	#
	# Bull-call spread
	#

	def bull_call_spread (self, underlying_symbol, option_symbol_0, quantity_0, option_symbol_1, quantity_1, duration='day'):
		r = requests.post(
			url 	= '{}/{}'.format(self.BASE_URL, self.ORDER_ENDPOINT),
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
			headers = self.REQUESTS_HEADERS
		);

		return r.json();


	# def extract_stock_symbol (self, occ_symbol):
	def extract_occ_underlying (self, occ_symbol):
		match = re.match(r'^([A-Z]){1,4}\d', occ_symbol);
		if match:
			return match.group(1);
		else:
			return None;


	def options_order (self, occ_symbol, order_type, side, quantity, underlying=False, limit_price=False, stop_price=False, duration='day'):
		'''
		Params:
			• occ_symbol = options contract (e.g. 'TER230915C00110000')
			• order_type = The type of order to be placed. One of: market, limit, stop, stop_limit
			• side = The side of the order. One of: buy_to_open, buy_to_close, sell_to_open, sell_to_close
			• quantity = Number of contracts to buy/sell
			• underlying = Underlying symbol. If not supplied, will be inferred from occ_symbol. (e.g. 'TER')
			• duration = Time the order will remain active. One of: day, gtc, pre, post
			• limit_price = Limit Price for limit or stop_limit orders
			• stop_price = Stop Price for stop or stop_limit orders

		Returns:
			• json from the requests.post call to the order endpoint

		Notes:
			• If order_type='limit' or order_type = 'stop_limit', then must specify limit_price
			• If order_type='stop' or order_type = 'stop_limit', then must specify stop_price

		Example:
			>>> options_order.options_order(occ_symbol='LMT240119C00260000', order_type='market', side='sell_to_close', quantity=10.0)
			# Returns: {'order': {'id': 8042606, 'status': 'ok', 'partner_id': '3a8bbee1-5184-4ffe-8a0c-294fbad1aee9'}}
		'''
		if not underlying:
			underlying = self.extract_occ_underlying(occ_symbol);

		r_data = {
			'class' 		: 'option',
			'symbol' 		: underlying,
			'option_symbol' : occ_symbol,
			'side' 			: side,
			'quantity' 		: quantity,
			'type' 			: order_type,
			'duration' 		: duration
		};

		if order_type in ['limit', 'stop_limit']:
			if not limit_price:
				print('Need limit price.');
				return None;
			r_data['price'] = limit_price;
		if order_type in ['stop', 'stop_limit']:
			if not stop_price:
				print('Need stop price.');
				return None;
			r_data['stop'] = stop_price;

		r = requests.post(
			url = '{}/{}'.format(self.BASE_URL, self.ORDER_ENDPOINT),
			data = r_data,
			headers = self.REQUESTS_HEADERS
		);

		return r.json();