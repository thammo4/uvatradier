import requests
import pandas as pd

from .base import Tradier

class Account (Tradier):
	def __init__ (self, account_number, auth_token, live_trade=False):
		Tradier.__init__(self, account_number, auth_token, live_trade);
		
		#
		# Account endpoints
		#

		self.PROFILE_ENDPOINT = "v1/user/profile"; 													# GET

		self.POSITIONS_ENDPOINT = "v1/accounts/{}/positions".format(account_number); 				# GET


		self.ACCOUNT_BALANCE_ENDPOINT 	= "v1/accounts/{}/balances".format(account_number); 		# GET
		self.ACCOUNT_GAINLOSS_ENDPOINT 	= "v1/accounts/{}/gainloss".format(account_number);  		# GET
		self.ACCOUNT_HISTORY_ENDPOINT 	= "v1/accounts/{}/history".format(account_number); 			# GET
		self.ACCOUNT_POSITIONS_ENDPOINT = "v1/accounts/{}/positions".format(account_number); 		# GET

		self.ACCOUNT_INDIVIDUAL_ORDER_ENDPOINT = "v1/accounts/{account_id}/orders/{order_id}"; 		# GET


		self.ORDER_ENDPOINT = "v1/accounts/{}/orders".format(account_number); 						# GET

	def get_user_profile(self):
		'''
		Fetch the user profile information from the Tradier Account API.

		This function makes a GET request to the Tradier Account API to retrieve the user profile
		information associated with the trading account linked to the provided credentials.
		The API response is expected to be in JSON format, containing details about the user profile.

		Returns:
		    pandas.DataFrame: A DataFrame containing user profile information.

		Example:
			# Initialize Account object
			account = Account(ACCOUNT_NUMBER, AUTH_TOKEN)

		    # Retrieve user profile information
		    user_profile = account.get_user_profile()
		    transposed_profile = user_profile.T  # Transpose the DataFrame for easy viewing.

		Example DataFrame (transposed):

			id              				id-lq-4h71lpfybz
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
			url 	= '{}/{}'.format(self.BASE_URL, self.PROFILE_ENDPOINT),
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
			# Initialize Account object
			account = Account(ACCOUNT_NUMBER, AUTH_TOKEN)

		    # Retrieve account balance information
		    account_balance = account.get_account_balance()
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
			url 	= '{}/{}'.format(self.BASE_URL, self.ACCOUNT_BALANCE_ENDPOINT),
			params 	= {},
			headers = self.REQUESTS_HEADERS
		);

		return pd.json_normalize(r.json()['balances']);


	def get_gainloss (self):
		'''
			Get cost basis information for a specific user account.
			This includes information for all closed positions.
			Cost basis information is updated through a nightly batch reconciliation process with tradier clearing firm.

			Returns:
				Pandas dataframe with columns [close_date, cost, gain_loss, gain_loss_percent, open_date, proceeds, quantity, symbol, term]

			Example Output:
				>>> account.get_gainloss().head()
						close_date      cost  gain_loss  gain_loss_percent                 open_date  proceeds  quantity              symbol  term
				0  2023-09-13T00:00:00.000Z  194700.0   -30600.0             -15.72  2023-08-25T00:00:00.000Z  164100.0      10.0  LMT240119C00260000    19
				1  2023-09-13T00:00:00.000Z   10212.2     -432.6              -4.24  2023-09-06T00:00:00.000Z    9779.6      20.0                KLAC     7
				2  2023-09-13T00:00:00.000Z    2300.0      175.0               7.61  2023-08-24T00:00:00.000Z    2475.0       1.0  HAL251219C00018000    20
				3  2023-09-13T00:00:00.000Z   20700.0     1620.0               7.83  2023-08-24T00:00:00.000Z   22320.0       9.0  HAL251219C00018000    20
				4  2023-09-06T00:00:00.000Z   16967.0     -193.0              -1.14  2023-09-01T00:00:00.000Z   16774.0     100.0                 TXN     5
		'''
		r = requests.get(
			url = '{}/{}'.format(self.BASE_URL, self.ACCOUNT_GAINLOSS_ENDPOINT),
			params = {},
			headers = self.REQUESTS_HEADERS
		);

		return pd.json_normalize(r.json()['gainloss']['closed_position']);


	def get_orders (self):
		'''
			This function returns a pandas DataFrame.
			Each row denotes a queued order. Each column contiains a feature_variable pertaining to the order.
			Transposed sample output has the following structure:

			>>> account.get_orders().T
			                                           0                         1
			id                                   8248093                   8255194
			type                              stop_limit                    market
			symbol                                   UNP                        CF
			side                                     buy                       buy
			quantity                                 3.0                      10.0
			status                                  open                    filled
			duration                                 day                       gtc
			price                                  200.0                       NaN
			avg_fill_price                           0.0                     87.39
			exec_quantity                            0.0                      10.0
			last_fill_price                          0.0                     87.39
			last_fill_quantity                       0.0                      10.0
			remaining_quantity                       3.0                       0.0
			stop_price                             200.0                       NaN
			create_date         2023-09-25T20:29:10.351Z  2023-09-26T14:45:00.155Z
			transaction_date    2023-09-26T12:30:19.152Z  2023-09-26T14:45:00.216Z
			class                                 equity                    equity
		'''

		r = requests.get(
			url='{}/{}'.format(self.BASE_URL, self.ORDER_ENDPOINT),
			params={'includeTags':'true'},
			headers=self.REQUESTS_HEADERS
		);

		if r.json()['orders'] == 'null':
			return 'You have no current orders.'

		return pd.json_normalize(r.json()['orders']['order'])

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
			# Initialize Account object
			account = Account('TRADIER_ACCOUNT_NUMBER', 'TRADIER_AUTH_TOKEN')

			# Retrieve all positions without filtering
			all_positions = account.get_positions()

			# Retrieve positions for specific symbols ('AAPL', 'GOOGL')
			specific_positions = account.get_positions(symbols=['AAPL', 'GOOGL'])

			# Retrieve only equities
			equities_positions = account.get_positions(equities=True)

			# Retrieve only options
			options_positions = account.get_positions(options=True)
		'''
		r = requests.get(url='{}/{}'.format(self.BASE_URL, self.ACCOUNT_POSITIONS_ENDPOINT), params={}, headers=self.REQUESTS_HEADERS);
		if r.json():
			positions_df = pd.DataFrame(pd.json_normalize(r.json()['positions']['position']));
			if symbols:
				positions_df = positions_df.query('symbol in @symbols');
			if equities:
				positions_df = positions_df[positions_df['symbol'].str.len() < 5];
				options = False;
			if options:
				positions_df = positions_df[positions_df['symbol'].str.len() > 5];
			return positions_df;