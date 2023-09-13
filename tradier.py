import os;
import dotenv;
import requests;
import numpy as np;
import pandas as pd;

import datetime;
from datetime import datetime, timedelta; 	# for fetching option expiries
import re; 									# parsing option symbols into constituent components

import schedule;
import time;

dotenv.load_dotenv();


#
# Fetch account credentials
#

ACCOUNT_NUMBER 	= os.getenv('tradier_acct');
AUTH_TOKEN 		= os.getenv('tradier_token');


class Tradier:
	def __init__ (self, account_number, auth_token):

		#
		# Define account credentials
		#

		self.ACCOUNT_NUMBER 	= account_number;
		self.AUTH_TOKEN 		= auth_token;
		self.REQUESTS_HEADERS 	= {'Authorization':'Bearer {}'.format(self.AUTH_TOKEN), 'Accept':'application/json'}

		
		#
		# Define base url for paper trading and individual API endpoints
		#

		self.SANDBOX_URL = 'https://sandbox.tradier.com';



class Account (Tradier):
	def __init__ (self, account_number, auth_token):
		Tradier.__init__(self, account_number, auth_token);
		
		#
		# Account endpoints
		#

		self.PROFILE_ENDPOINT = "v1/user/profile"; 										# GET

		self.POSITIONS_ENDPOINT = "v1/accounts/{}/positions".format(ACCOUNT_NUMBER); 				# GET


		self.ACCOUNT_BALANCE_ENDPOINT 	= "v1/accounts/{}/balances".format(ACCOUNT_NUMBER); 		# GET
		self.ACCOUNT_GAINLOSS_ENDPOINT 	= "v1/accounts/{}/gainloss".format(ACCOUNT_NUMBER);  		# GET
		self.ACCOUNT_HISTORY_ENDPOINT 	= "v1/accounts/{}/history".format(ACCOUNT_NUMBER); 			# GET
		self.ACCOUNT_POSITIONS_ENDPOINT = "v1/accounts/{}/positions".format(ACCOUNT_NUMBER); 		# GET

	def get_user_profile(self):
		'''
		Fetch the user profile information from the Tradier Account API.

		This function makes a GET request to the Tradier Account API to retrieve the user profile
		information associated with the trading account linked to the provided credentials.
		The API response is expected to be in JSON format, containing details about the user profile.

		Returns:
		    pandas.DataFrame: A DataFrame containing user profile information.

		Example:
		    # Retrieve user profile information
		    user_profile = get_user_profile()
		    transposed_profile = user_profile.T  # Transpose the DataFrame for easy viewing.

		Example DataFrame (transposed):

			id              				id-sb-2r01lpprbg
			name               				Fat Albert
			account.account_number     		ABC1234567
			account.classification   		individual
			account.date_created  			2021-06-23T22:04:20.000Z
			account.day_trader              False
			account.option_level                6
			account.status                 	active
			account.type                   	margin
			account.last_update_date 		2021-06-23T22:04:20.000Z
		'''
		r = requests.get(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.PROFILE_ENDPOINT),
			params 	= {},
			headers = self.REQUESTS_HEADERS
		);

		return pd.json_normalize(r.json()['profile']);


	def get_account_balance(self):
		'''
		Fetch the account balance information from the Tradier Account API.

		This function makes a GET request to the Tradier Account API to retrieve the account
		balance information for the trading account associated with the provided credentials.
		The API response is expected to be in JSON format, containing details about the account
		balance.

		Returns:
		    pandas.DataFrame: A DataFrame containing account balance information.

		Example:
		    # Retrieve account balance information
		    account_balance = get_account_balance()
		    transposed_balance = account_balance.T  # Transpose the DataFrame for easy viewing.

		Example DataFrame (transposed):
		                            0
			option_short_value       -147.0
			total_equity           74314.82
			account_number       ABC1234567
			account_type             margin
			close_pl                      0
			current_requirement    17595.08
			equity                        0
			long_market_value      34244.16
			market_value           34097.16
			open_pl               -225300.265
			option_long_value        1054.0
			option_requirement       1000.0
			pending_orders_count          8
			short_market_value         -147.0
			stock_long_value        33190.16
			total_cash             40217.66
			uncleared_funds               0
			pending_cash            16892.9
			margin.fed_call               0
			margin.maintenance_call       0
			margin.option_buying_power 38919.84
			margin.stock_buying_power  77839.68
			margin.stock_short_value       0
			margin.sweep                   0
		'''
		r = requests.get(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.ACCOUNT_BALANCE_ENDPOINT),
			params 	= {},
			headers = self.REQUESTS_HEADERS
		);

		return pd.json_normalize(r.json()['balances']);


	def get_positions(self, symbols=False, equities=False, options=False):
		'''
		Fetch and filter position data from the Tradier Account API.

		This function makes a GET request to the Tradier Account API to retrieve position
		information related to a trading account. The API response is expected to be in
		JSON format, containing details about the positions held in the account.

		Args:
		    symbols (list, optional): A list of trading symbols (e.g., stock ticker symbols)
		                              to filter the position data. If provided, only positions
		                              matching these symbols will be included.
		    equities (bool, optional): If True, filter the positions to include only equities
		                              (stocks) with symbols less than 5 characters in length.
		                              If False, no filtering based on equities will be applied.
		    options (bool, optional): If True, filter the positions to include only options
		                              with symbols exceeding 5 characters in length.
		                              If False, no filtering based on options will be applied.

		Returns:
		    pandas.DataFrame: A DataFrame containing filtered position information based on
		                      the specified criteria.

		Example:
		    # Retrieve all positions without filtering
		    all_positions = get_positions()

		    # Retrieve positions for specific symbols ('AAPL', 'GOOGL')
		    specific_positions = get_positions(symbols=['AAPL', 'GOOGL'])

		    # Retrieve only equities
		    equities_positions = get_positions(equities=True)

		    # Retrieve only options
		    options_positions = get_positions(options=True)
		'''
		r = requests.get(url='{}/{}'.format(self.SANDBOX_URL, self.ACCOUNT_POSITIONS_ENDPOINT), params={}, headers=self.REQUESTS_HEADERS);

		positions_df = pd.DataFrame(r.json()['positions']['position']);

		if symbols:
		    positions_df = positions_df.query('symbol in @symbols');

		if equities:
		    positions_df = positions_df[positions_df['symbol'].str.len() < 5];
		    options = False;

		if options:
		    positions_df = positions_df[positions_df['symbol'].str.len() > 5];

		return positions_df;


class Quotes (Tradier):
	def __init__ (self, account_number, auth_token):
		Tradier.__init__(self, account_number, auth_token);

		#
		# Quotes endpoints for market data about equities
		#

		self.QUOTES_ENDPOINT 				= "v1/markets/quotes"; 											# GET (POST)
		self.QUOTES_HISTORICAL_ENDPOINT 	= "v1/markets/history"; 										# GET
		self.QUOTES_TIMESALES_ENDPOINT 		= "v1/markets/timesales"; 										# GET

	def get_historical_quotes (self, symbol, interval='daily', start_date=False, end_date=False):

		'''
		Fetch historical stock data for a given symbol from the Tradier Account API.

		This function makes a GET request to the Tradier Account API to retrieve historical stock
		data for a specified symbol within a specified time interval.

		Args:
			symbol (str): The trading symbol of the stock (e.g., 'AAPL', 'MSFT') for which you want
			              to retrieve historical data.
			interval (str, optional): The time interval for historical data. Default is 'daily'.
			start_date (str, optional): The start date for historical data in the format 'YYYY-MM-DD'.
			                           If not provided, the function will default to the most recent Monday.
			end_date (str, optional): The end date for historical data in the format 'YYYY-MM-DD'.
			                         If not provided, the function will default to the current date.

		Returns:
			pandas.DataFrame: A DataFrame containing historical stock data for the specified symbol.

		Example:
			# Create a Quotes instance
			q = Quotes(ACCOUNT_NUMBER, AUTH_TOKEN)

			# Retrieve historical stock data for symbol 'BIIB'
			historical_data = q.get_historical_quotes(symbol='BIIB')

			Sample Output:
			         date    open     high     low   close   volume
			0  2023-08-28  265.40  266.470  263.54  265.05   359872
			1  2023-08-29  265.35  268.150  265.11  268.00   524972
			2  2023-08-30  268.84  269.460  265.25  267.18   552728
			3  2023-08-31  266.83  269.175  265.32  267.36  1012842
			4  2023-09-01  269.01  269.720  266.91  267.17   522401
		'''

		#
		# Helper function used to index the start of the trading week
		#

		def last_monday (input_date):
			'''
			Find the date of the previous Monday for a given input date.

			Args:
				input_date (datetime.date): the input date

			Returns:
				datetime.date: The date of the previous Monday.
			'''

			return (input_date - timedelta(days=(input_date.weekday())));

		if not end_date:
			end_date = datetime.today().strftime('%Y-%m-%d');

		if not start_date:
			tmp = datetime.strptime(end_date, '%Y-%m-%d');
			start_date = last_monday(tmp).strftime('%Y-%m-%d');

		r = requests.get(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.QUOTES_HISTORICAL_ENDPOINT),
			params 	= {
				'symbol' 	: symbol,
				'interval' 	: interval,
				'start' 	: start_date,
				'end' 		: end_date
			},
			headers = self.REQUESTS_HEADERS
		);

		return pd.DataFrame(r.json()['history']['day']);

	def get_quote_day (self, symbol, last_price=False):
		'''
		Fetch the current quote data for a given symbol from the Tradier Account API.

		This function makes a GET request to the Tradier Account API to retrieve the current quote
		data for a specified symbol.

		Args:
			symbol (str): The trading symbol of the stock (e.g., 'AAPL', 'MSFT') for which you want
			              to retrieve the current quote data.
			last_price (bool, optional): If True, only fetch the last price of the symbol. Default is False.

		Returns:
			pandas.DataFrame or float: A DataFrame containing the current quote data for the specified symbol
									   or just the last price as a float if last_price is set to True.

		Example:
			# Retrieve current quote data for symbol 'CCL' and transpose the DataFrame for easy viewing
			quote_data = q.get_quote_day(symbol='CCL').T

			Sample Output:
			                           0
			symbol                 CCL
			description  Carnival Corp
			exch                     N
			type                 stock
			last                 15.73
			change               -0.09
			volume            16767253
			open                 15.83
			high                 16.06
			low                  15.58
			close                15.73
			bid                   15.7
			ask                  15.73
			change_percentage    -0.57
			average_volume    39539044
			last_volume              0
			trade_date   1693609200001
			prevclose            15.82
			week_52_high         19.55
			week_52_low           6.11
			bidsize                 11
			bidexch                  P
			bid_date     1693612800000
			asksize                 29
			askexch                  P
			ask_date     1693612764000
			root_symbols           CCL

			# Retrieve only the last price for symbol 'CCL'
			last_price = q.get_quote_day(symbol='CCL', last_price=True)
			Sample Output: 15.73
		'''

		r = requests.get(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.QUOTES_ENDPOINT),
			params 	= {'symbols':symbol, 'greeks':'false'},
			headers = self.REQUESTS_HEADERS
		);

		df_quote = pd.json_normalize(r.json()['quotes']['quote']);

		if last_price:
			return float(df_quote['last']);

		return df_quote;


class OptionsData (Tradier):
	def __init__ (self, account_number, auth_token):
		Tradier.__init__(self, account_number, auth_token);

		#
		# Option data endpoints
		#

		self. OPTIONS_STRIKE_ENDPOINT 	= "v1/markets/options/strikes"; 							# GET
		self. OPTIONS_CHAIN_ENDPOINT 	= "v1/markets/options/chains"; 								# GET
		self. OPTIONS_EXPIRY_ENDPOINT 	= "v1/markets/options/expirations"; 						# GET
		self. OPTIONS_SYMBOL_ENDPOINT 	= "v1/markets/options/lookup"; 								# GET


	#
	# Fetch all option chain data for a single day of contract expirations
	#

	def get_chain_day (self, symbol, expiry='', strike=False, strike_low=False, strike_high=False, option_type=False):
		'''
			This function returns option chain data for a given symbol.
			All contract expirations occur on the same expiry date
		'''

		#
		# Set the contract expiration date to the nearest valid date
		#

		if not expiry:
			expiry = self.get_expiry_dates(symbol)[0];

		#
		# Define request object for given symbol and expiration
		#

		r = requests.get(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.OPTIONS_CHAIN_ENDPOINT),
			params 	= {'symbol':symbol, 'expiration':expiry, 'greeks':'false'},
			headers = self.REQUESTS_HEADERS
		);

		#
		# Convert returned json -> pandas dataframe
		#

		option_df = pd.DataFrame(r.json()['options']['option']);


		#
		# Remove columns which have the same value for every row
		#

		cols_to_drop = option_df.nunique()[option_df.nunique() == 1].index;
		option_df = option_df.drop(cols_to_drop, axis=1);

		#
		# Remove columns which have NaN in every row
		#

		cols_to_drop = option_df.nunique()[option_df.nunique() == 0].index;
		option_df = option_df.drop(cols_to_drop, axis=1);


		#
		# Remove description column because its information is redundant
		#

		cols_to_drop = ['description'];
		option_df = option_df.drop(cols_to_drop, axis=1);


		#
		# Filter rows per strike_low and strike_high
		#

		if strike_low:
			option_df = option_df.query('strike >= @strike_low');

		if strike_high:
			option_df = option_df.query('strike <= @strike_high');

		if strike:
			option_df = option_df.query('strike == @strike');

		if option_type in ['call', 'put']:
			option_df = option_df.query('option_type == @option_type');


		if option_type:
			if option_type in ['call', 'put']:
				option_df = option_df.query('option_type == @option_type');

		#
		# Return the resulting dataframe whose rows are individual contracts with expiration `expiry`
		#

		return option_df;


	def get_expiry_dates (self, symbol, strikes=False):
		'''
		Get the expiry dates for options on a given symbol.

		Args:
			symbol (str): The symbol for which to retrieve expiry dates.
			strikes (bool, optional): Whether to include strike prices for each expiry date. Defaults to False.

		Returns:
			If strikes=False 	-> returns list or list of dict: A list of expiry dates in the format 'YYYY-MM-DD'.
			If strikes=True 	-> returns a list of dictionaries with expiry date and associated strike prices.

		Example:
			>>> options = OptionsData(ACCOUNT_NUMBER, AUTH_TOKEN)
			>>> options.get_expiry_dates(symbol='DFS')
			['2023-09-08', '2023-09-15', '2023-09-22', '2023-09-29', '2023-10-06', '2023-10-13', '2023-10-20', '2023-11-17', '2024-01-19', '2024-04-19', '2024-06-21', '2025-01-17']

			>>> options.get_expiry_dates(symbol='DFS', strikes=True)
			[{'date': '2023-09-08', 'strikes': {'strike': [59.0, 60.0, 61.0, ...]}, {'date': '2023-09-15', 'strikes': {'strike': [55.0, 60.0, ...}}, ...]
		'''

		r = requests.get(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.OPTIONS_EXPIRY_ENDPOINT),
			params 	= {'symbol':symbol, 'includeAllRoots':True, 'strikes':str(strikes)},
			headers = self.REQUESTS_HEADERS
		);

		if r.status_code != 200:
			return 'wtf';

		expiry_dict = r.json()['expirations'];

		# Without strikes, we can get a list of dates
		if strikes == False:
			return expiry_dict['date'];

		# Otherwise, return a list whose elements are dicts with format {'date':[list_of_strikes]}
		return expiry_dict['expiration'];


	#
	# This function returns a list of symbols. Each element has a format
	# 	COP240216C00115000
	#
	# i.e.
	#
	# 	COP 240216 C 00115000
	#

	def get_options_symbols (self, symbol, df=False):
		'''
			This function provides a convenient wrapper to fetch option symbols
			for a specified symbol

			If df=False, then a list of OCC options symbols is returned.
			For an n-element list, if i=0,...,(n-1), then every (option_list[i-1], option_list[i]) pair of elements represents a pair of call/put options.

			If df=True, then a pandas.DataFrame object is returned.
			Each row of the dataframe represents a single put or call contract.
			The first column is the OCC symbol. The subsequent columns are the parsed values of the OCC symbol.
		'''

		#
		# Helper function to convert the get_option_symbols list into a dataframe
		#

		def symbol_list_to_df (option_list):
			'''
				This is a helper function called from get_option_symbols.
				It will parse a list of option symbols into their constituent components
				For example:
					option_symbol
						= [underlying_symbol, expiry_date, option_type, option_id]
						= [LMT, 240119, C, 00300000]
			'''
			parsed_options = []

			for option in option_list:
			    match = re.match(r'([A-Z]+)(\d{6})([CP])(\d+)', option)
			    if match:
			        root_symbol, expiration_date, option_type, strike_price = match.groups()
			        parsed_options.append({
			        'symbol' 			: option,
			        'root_symbol' 		: root_symbol,
			        'expiration_date' 	: expiration_date,
			        'option_type' 		: option_type,
			        'strike_price' 		: strike_price
			        })
			return pd.DataFrame(parsed_options);


		#
		# Helper function to turn the option dates into standard date format
		#

		def parse_option_expiries (expiry_list):
			'''
				Helper function to turn the option dates into standard date format
			'''

			formatted_expiries = [];
			for x in expiry_list:
				formatted_expiries.append(datetime.strptime(x, '%y%m%d').strftime('%Y-%m-%d'));

			return formatted_expiries;


		r = requests.get(
			url 		= '{}/{}'.format(self.SANDBOX_URL, self.OPTIONS_SYMBOL_ENDPOINT),
			params 		= {'underlying':symbol},
			headers 	= self.REQUESTS_HEADERS
		);

		option_list = r.json()['symbols'][0]['options'];

		if df:
			option_df = symbol_list_to_df(option_list);
			option_df['expiration_date'] = parse_option_expiries(option_df['expiration_date']);
			return option_df;

		return option_list;



class EquityOrder (Tradier):
	def __init__ (self, account_number, auth_token):
		Tradier.__init__(self, account_number, auth_token);

		#
		# Order endpoint
		#

		self.ORDER_ENDPOINT = "v1/accounts/{}/orders".format(self.ACCOUNT_NUMBER); # POST


	#
	# Post data for equity market order
	#

	def equity_market_order (self, symbol, side, quantity, duration='day'):
		'''
			This function will place a simple market order for the supplied symbol.
			By default, the order is good for the day. Per the nature of market orders, it should be filled.

			Parameter Notes:
				side 		= buy, buy_to_cover, sell, sell_short
				duration 	= day, gtc, pre, post
		'''

		r = requests.post(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
			params 	= {
				'class'		: 'equity',
				'symbol' 	: symbol,
				'side' 		: side,
				'quantity' 	: quantity,
				'type' 		: 'market',
				'duration' 	: duration
			},
			headers = self.REQUESTS_HEADERS
		);

		return r.json();



	#
	# Post data for equity limit order
	#

	def equity_limit_order (self, symbol, side, quantity, limit_price, duration='day'):
		'''
			This function places a limit order to buy/sell the given symbol at the specified limit_price (or better).
			Recall that a limit order guarantees the execution price. However, the order might not execute at all.

			Parameter Notes:
				side 		= buy, buy_to_cover, sell, sell_short
				duration 	= day, gtc, pre, post
		'''

		r = requests.post(
			url = '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
			data = {
				'class' 	: 'equity',
				'symbol' 	: symbol,
				'side' 		: side,
				'quantity' 	: quantity,
				'type' 		: 'limit',
				'duration' 	: duration,
				'price' 	: limit_price
			},
			headers = self.REQUESTS_HEADERS
		);

		return r.json();


	#
	# Post data for equity stop-loss or stop-entry orders
	#

	def equity_stop_order (self, symbol, side, quantity, stop_price, duration='day'):
		'''
			This function places a stop-loss or stop-entry order to buy/sell equities.
			Recall that a stop order will trigger in the direction of the stock's movement

			Parameter Notes:
				side 		= buy, buy_to_cover, sell, sell_short
				duration 	= day, gtc, pre, post
		'''

		r = requests.post(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
			data 	= {
				'class' 	: 'equity',
				'symbol' 	: symbol,
				'side' 		: side,
				'quantity' 	: quantity,
				'type' 		: 'stop',
				'duration' 	: duration,
				'stop' 		: stop_price
			},
			headers = self.REQUESTS_HEADERS
		);

		return r.json();


	#
	# Post data for equity stop-limit order
	#

	def equity_stop_limit_order (self, symbol, side, quantity, stop_price, limit_price, duration='day'):
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
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
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
			headers = self.REQUESTS_HEADERS
		);

		return r.json();



class OptionsOrder (Tradier):
	def __init__ (self, account_number, auth_token):
		Tradier.__init__(self, account_number, auth_token);

		#
		# Order endpoint
		#

		self.ORDER_ENDPOINT = "v1/accounts/{}/orders".format(ACCOUNT_NUMBER); # POST


	#
	# Bear-put spread
	#

	def bear_put_spread (self, underlying, option0, quantity0, option1, quantity1, duration='day'):
		r = requests.post(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
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
			Bear call spread legs:
				• short call with K1 ≥ S -> receive premium d1
				• long call with K2 > K1 ≥ S -> pay premium d2 ; d2 < d1
				• upfront credit of (d1-d2)
		'''
		r = requests.post(
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
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
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
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
			url 	= '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
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


	#
	# Option contract market order
	#

	def option_market_order (self, underlying_symbol, option_symbol, side, quantity, duration='day'):
		'''
			This function places a simple market order to long/short an option contract.
			Valid argument values:
				side 		= buy_to_open, buy_to_close, sell_to_open, sell_to_close
				duration 	= day, gtc, pre, post
		'''
		r = requests.post(
			url = '{}/{}'.format(self.SANDBOX_URL, self.ORDER_ENDPOINT),
			data = {
				'class' 		: 'option',
				'symbol' 		: underlying_symbol,
				'option_symbol' : option_symbol,
				'side' 			: side,
				'quantity' 		: quantity,
				'type' 			: 'market',
				'duration' 		: duration
			},
			headers = self.REQUESTS_HEADERS
		);

		print(r.json());



#
# Initialize objects for testing
#

account = Account(ACCOUNT_NUMBER, AUTH_TOKEN);
quotes 	= Quotes(ACCOUNT_NUMBER, AUTH_TOKEN);
options = OptionsData(ACCOUNT_NUMBER, AUTH_TOKEN);


options_order = OptionsOrder(ACCOUNT_NUMBER, AUTH_TOKEN);