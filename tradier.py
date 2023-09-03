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





















































































































































































	def get_gainloss(self, symbols='', results_limit='', sort_dates='closeDate', sort_symbols='', start_date='', end_date=''):
		'''
		Fetch gain/loss information for closed positions from the Tradier Account API.

		This function makes a GET request to the Tradier Account API to retrieve information;
		about gain/loss for closed positions in the trading account associated with the provided;
		credentials. The API response is expected to be in JSON format, containing details about;
		the gain/loss for closed positions.

		Args:
			symbols (str, optional): A comma-separated string of trading symbols to filter the;
			gain/loss data. If provided, only positions with matching;
			symbols will be included.
			results_limit (str, optional): Limit the number of results returned. If provided,;
			the function will retrieve the specified number of results.
			sort_dates (str, optional): Specify how to sort the results by date ('closeDate' or 'openDate').
			sort_symbols (str, optional): Specify how to sort the results by symbols.
			start_date (str, optional): Filter the results to include only positions closed on or;
			after the specified start date (YYYY-MM-DD).
			end_date (str, optional): Filter the results to include only positions closed on or;
			before the specified end date (YYYY-MM-DD).

		Returns:
			pandas.DataFrame: A DataFrame containing gain/loss information for closed positions.

		Example:
			# Retrieve all closed position gain/loss without filtering;
			>>> Account.get_gainloss()
						 close_date    cost  gain_loss  gain_loss_percent                 open_date  proceeds  quantity symbol  term;
			0  2023-08-31T00:00:00.000Z  3443.9     -140.9              -4.09  2023-07-24T00:00:00.000Z    3303.0      10.0   MSFT    38;

			# Retrieve gain/loss for specific symbols ('AAPL', 'GOOGL');
			>>> Account.get_gainloss(symbols='AAPL,GOOGL');

			# Retrieve gain/loss for positions closed after a specific date;
			>>> Account.get_gainloss(start_date='2023-01-01');

			# Retrieve gain/loss with custom sorting and result limit;
			>>> Account.get_gainloss(sort_dates='closeDate', results_limit='10');
		'''
		params_dict = {'sortBy': sort_dates};

		if results_limit:
			params_dict['limit'] = results_limit;

		if sort_symbols:
			params_dict['sort'] = sort_symbols;

		if start_date:
			params_dict['start'] = start_date;

		if end_date:
			params_dict['end'] = end_date;

		r = requests.get(
			url='{}/{}'.format(self.SANDBOX_URL, self.ACCOUNT_GAINLOSS_ENDPOINT),
			params=params_dict,
			headers=self.REQUESTS_HEADERS
		);

		gainloss_df = pd.json_normalize(r.json()['gainloss']['closed_position']);

		return gainloss_df;