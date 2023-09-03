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

		self.PROFILE_ENDPOINT 			= "v1/user/profile"; 										# GET

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
		                             0
			id              id-sb-2r01lpprbg
			name               Thomas Hammons
			account.account_number     VA36593574
			account.classification   individual
			account.date_created  2021-06-23T22:04:20.000Z
			account.day_trader              False
			account.option_level                6
			account.status                 active
			account.type                   margin
			account.last_update_date  2021-06-23T22:04:20.000Z
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
			account_number       VA36593574
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