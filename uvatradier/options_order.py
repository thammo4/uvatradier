from .base import Tradier

from typing import Optional, Dict, Any
import requests
import pandas as pd
import re


#
# Custom Exception Class - Indicate Malformed Parameters for Intended Order
#

class InvalidOrderParameterError (Exception):
	pass;


#
# Custon Exception Class - Indicate Issues Extracting Underlying Ticker Symbol from OCC Symbol
#

class InvalidOCCSymbolError (Exception):
	pass;


#
# Custom Exception Class - Indicate Issues with API Requests
#

class APIRequestError (Exception):
	pass;



#
# Define OptionsOrder Class - Implements Calls to Tradier Trading API for Options
#

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


	def extract_occ_underlying (self, occ_symbol):
		try:
			pattern = r'^([A-Z]+(?:[A-Z])?)(?=[0-9]{6}[CP])';
			match = re.match(pattern, occ_symbol);
			if match:
				underlying = match.group(1);
				if underlying:
					return underlying;
				else:
					return None;
		except Exception as e:
			raise InvalidOCCSymbolError(f"No underlying extracted for OCC: {occ_symbol}. Error: {str(e)}");


	def options_order (self, occ_symbol, order_type, side, quantity, underlying=None, limit_price=None, stop_price=None, duration='day'):
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

		valid_order_types = {'market', 'limit', 'stop', 'stop_limit'};
		valid_sides = {'buy_to_open', 'buy_to_close', 'sell_to_open', 'sell_to_close'};
		valid_durations = {'day', 'gtc', 'pre', 'post'};


		#
		# Check that order parameters are legit
		#

		if order_type not in valid_order_types:
			raise InvalidOrderParameterError(f"Bad order_type. Valid: {', '.join(valid_order_types)}");
		if side not in valid_sides:
			raise InvalidOrderParameterError(f"Bad side. Valid: {', '.join(valid_sides)}");
		if duration not in valid_durations:
			raise InvalidOrderParameterError(f"Bad duration. Valid: {', '.join(valid_durations)}");
		if not isinstance(quantity, int):
			raise InvalidOrderParameterError(f"Quantity non-integer. Valid: positive integer");
		if quantity <= 0:
			 raise InvalidOrderParameterError(f"Quantity non-positive. Valid: quantity > 0");


		#
		# Infer underlying symbol from OCC Symbol [if underlying not provided]
		#

		if not underlying:
			try:
				underlying = self.extract_occ_underlying(occ_symbol);
			except InvalidOCCSymbolError as e:
				raise InvalidOrderParameterError(f"Bad OCC symbol extraction: {str(e)}");

		r_data = {
			'class' 		: 'option',
			'symbol' 		: underlying,
			'option_symbol' : occ_symbol,
			'side' 			: side,
			'quantity' 		: quantity,
			'type' 			: order_type,
			'duration' 		: duration
		};

		if order_type in {'limit', 'stop_limit'}:
			if limit_price is None or limit_price <= 0:
				raise InvalidOrderParameterError("Bad (stop) limit price. Valid: [floats] limit_price > 0, stop_price > 0");
			r_data['price'] = limit_price;

		if order_type in {'stop', 'stop_limit'}:
			if stop_price is None or stop_price <= 0:
				raise InvalidOrderParameterError("Bad (stop) limit price. Valid: [floats] limit_price > 0, stop_price > 0");
			r_data['stop'] = stop_price;

		try:
			r = requests.post(
				url = f"{self.BASE_URL}/{self.ORDER_ENDPOINT}",
				data = r_data,
				headers = self.REQUESTS_HEADERS
			);
			r.raise_for_status();
			return r.json();
		except requests.RequestException as e:
			raise requests.RequestException(f"API Request Failed: {str(e)}");

		return r.json();


	#
	# Multileg Order
	# • Construct options order with ≤ 4 legs
	# • Use to execute orders for options strategy trades
	#

	def multileg_order (self, occ_symbols, sides, quantities, order_type, limit_price=None, duration='day', underlying=None):
		'''
		Place a multileg order with up to 4 legs. This order type allows for simple and complex option strategies.

		Params:
			• occ_symbols (list): list of strings containing the constituent OCC symbols of the multileg trade.
			• sides (list): list of string containing each leg's trade side. One of: buy_to_open, buy_to_close, sell_to_open, sell_to_close.
			• quantities (list): list of integer values denoting the number of contracts for each leg of the trade.
			• order_type (str): instruct broker how to execute trade. One of: market, debit, credit, even.
			• duration (str, default='day'): how long to keep the order alive while trying to fill it. One of: day, gtc, pre, post.
			• limit_price (numeric: int, float): execution price threshold for credit and debit (spread) orders.
				• If order_type='market' or order_type='even' -> limit_price is optional.
				• Debit Spreads: 	order_type='debit' 	-> limit_price = MAXimum willing to pay to execute trade.
				• Credit Spreads: 	order_type='credit' -> limit_price = MINimum premiumn willing to receive to execute trade.
			• underlying (str, optional): underlying symbol off of which the option contracts are derived.
				• If not supplied, it will be inferred from the OCC symbol.

		Returns:
			• json from the requests.post call to the order endpoint

		Notes:
			• Number of options to trade cannot exceed four.
			• All contracts in the trade share a common underlying.
			• For list typed arguments, the ordinal position of elements across occ_symbols, sides, and quantities correspond to each other.
				• E.g the 0th element of occ_symbols will have a side corresponding to the 0th element of sides and a quantity given by the 0th element of quantities
		Example:

			>>> # Bull Put [Credit] Spread - Multileg Options Order
			>>>
			>>> pd.DataFrame([short_leg,long_leg])
			               symbol   last   bid   ask  strike option_type
			30  PG240816P00175000  10.05  9.30  10.6   175.0         put
			28  PG240816P00170000   4.85  5.35   5.5   170.0         put
			>>> options_order.multileg_order(
				occ_symbols = [short_leg['symbol'], long_leg['symbol']],
				sides = ['sell_to_open', 'buy_to_open'],
				quantities = [1,1],
				order_type = 'credit',
				limit_price = .975 * (short_leg['bid'] - long_leg['ask']),
				duration='gtc'
			)
			# Returned JSON (dict)
			{'order': {'id': 13121888, 'status': 'ok', 'partner_id': '3a8bbee1-5184-4ffe-8a0c-294fbad1aee9'}}

		'''

		valid_order_types = {'market', 'debit', 'credit', 'even'};
		valid_durations = {'day', 'gtc', 'pre', 'post'};
		valid_sides = {'buy_to_open', 'buy_to_close', 'sell_to_open', 'sell_to_close'};

		#
		# Fleece the input arguments to check that they are valid/conform to Tradier's specs for multileg trade.
		#

		if not all(isinstance(occ, str) for occ in occ_symbols):
			raise InvalidOrderParameterError("Bad symbols. OCCs for options must be strings.");


		if not all(side in valid_sides for side in sides):
			raise InvalidOrderParameterError(f"Bad order side. Valid: {', '.join(valid_sides)}");

		if not all(isinstance(quantity, int) and quantity > 0 for quantity in quantities):
			raise InvalidOrderParameterError("Bad quantity. Valid: [int] quantities > 0");

		if len(occ_symbols) != len(sides) or len(occ_symbols) != len(quantities):
			print('Need to pass the same number for: occ_symbols, quantities, sides');
			return dict();

		if order_type not in valid_order_types:
			raise InvalidOrderParameterError(f"Bad order type. Valid: {', '.join(valid_order_types)}");

		if duration not in valid_durations:
			raise InvalidOrderParameterError(f"Bad duration. Valid: {', '.join(valid_durations)}");

		if order_type in {'debit', 'credit'} and (limit_price is None or limit_price <= 0):
			raise InvalidOrderParameterError("Bad limit price. Valid: [float] limit_price > 0");


		if not underlying:
			try:
				underlying = self.extract_occ_underlying(occ_symbols[0]);
			except Exception as e:
				raise InvalidOrderParameterError(f"Bad OCC Symbol extraction: {str(e)}");

		r_data = {
			'class': 'multileg',
			'duration':duration,
			'type':order_type,
			'symbol':underlying
		};

		if limit_price is not None:
			r_data['price'] = str(limit_price);

		for i, (occ, side, quantity) in enumerate(zip(occ_symbols, sides, quantities)):
			r_data[f"option_symbol[{i}]"] = occ;
			r_data[f"side[{i}]"] = side;
			r_data[f"quantity[{i}]"] = str(quantity);


		#
		# Make API Call to Order API to Send Trade to Tradier
		#

		try:
			r = requests.post(
				url = f"{self.BASE_URL}/{self.ORDER_ENDPOINT}",
				data = r_data,
				headers = self.REQUESTS_HEADERS
			);
			r.raise_for_status();

		except requests.RequestException as e:
			if e.response is not None:
				try:
					e_msg = f"Failed API Request: {str(e)}";
					e_msg += f"\nDetails: {e.response.json()}";
				except ValueError:
					e_msg += f"\nResponse: {e.response.text}";
			raise APIRequestError(e_msg);

		return r.json();

	#
	# Combination Order
	# • One equity leg
	# • ≤ Two option legs
	#

	# def combo_order (self, occ_symbols, sides, quantities, limit_prices=None, duration='day'):
	# 	print('hello, combo order!');


	#
	# One-Triggers-Other Order (OTO)
	# • Two separate orders sent simultaneously to Tradier
	#

	# def oto_order (self, order_types, occ_symbols, sides, quantities, limit_prices=None, stop_prices=None, duration='day'):
	# 	print('hello, oto order!');


	#
	# One-Cancels-Other Order (OCO)
	# • Two separate orders sent simultaneously to Tradier
	# • Constraints:
	# 	• Order types must be different: type[0] ≠ type[1]
	# 	• Two equitiy orders require the same underlying symbol
	# 	• Two options orders require the same OCC symbol
	# `	• Per-leg specified durations must match: duration[0] = duration[1]
	#

	# def oco_order (self, order_types, occ_symbols, sides, quantities, limit_prices=None, stop_prices=None, duration='day'):
	# 	print('hello, oco order!');



	#
	# One-Triggers-One-Cancels-Other Order (OTOCO)
	# • Three separate orders sent simultaneously to Tradier
	# • Constraints:
	# 	• Three equity orders requires symbol[2] = symbol[3]
	# 	• Three options orders requires occ_symbol[2] = occ_symbol[3]
	# 	• Leg two/three must have different order types: order_type[2] ≠ order_type[3]
	# 	• Per-leg duration requires duration[2] = duration[3]
	#

	# def otoco_order (self, order_types, occ_symbols, sides, quantities, limit_prices=None, stop_prices=None, duration='day'):
	# 	print('hello, otoco order!');