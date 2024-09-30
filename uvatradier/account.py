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

	def get_gainloss (self, page=1, limit=100, sort_by='closeDate', sort_direction='desc', start_date=None, end_date=None, symbol_filter=None):
		'''
			Args (All Optional):
				• page (int): Page from which to begin returning records.
				• limit (int): Number of records to return on each page.
				• sort_by (str): Field by which results will be sorted. One of: 'openDate', 'closeDate'
				• sort_direction (str): Direction in which the `sortBy` field will be sorted. One of: 'asc', 'desc'.
				• start_date (str, YYYY-mm-dd): Date from which records are returned.
				• end_date (str, YYYY-mm-dd): Date until which records are returned.
				• symbol_filter (str): Alphanumeric character used to filter returned results.

			Returns:
				• pandas.DataFrame:
					(DF) A DataFrame containing cost basis related information pertaining to positions which have been closed.

			Notes:
				• The `symbol_filter` argument will return any row whose ticker symbol either is or contains the `symbol_filter` argument.

			Example 1:
				# Instantiate Account object
				acct = Account(tradier_acct, tradier_token)

				# Retrieve the most recent 100 records sorted from most->least recent date on which position was closed.
				acct.get_gainloss()
				                  close_date     cost  gain_loss  gain_loss_percent  ... proceeds  quantity  symbol term
				0   2024-09-27T00:00:00.000Z  1933.10     343.90              17.79  ...  2277.00      10.0    AAPL  116
				1   2024-09-16T00:00:00.000Z    28.66      -0.53              -1.85  ...    28.13       1.0     HAL    7
				2   2024-09-16T00:00:00.000Z    37.52      -1.16              -3.09  ...    36.36      -1.0       B    7
				3   2024-09-09T00:00:00.000Z   172.80       0.00               0.00  ...   172.80      40.0     VVR   10
				4   2024-09-09T00:00:00.000Z   121.25      15.52              12.80  ...   136.77      97.0     VLD   10
				..                       ...      ...        ...                ...  ...      ...       ...     ...  ...
				95  2024-08-30T00:00:00.000Z   170.03       0.48               0.28  ...   170.51       1.0      PG    1
				96  2024-08-30T00:00:00.000Z     6.08      -0.42              -6.91  ...     5.66      32.0    OPTT    8
				97  2024-08-30T00:00:00.000Z  1125.74       7.84               0.70  ...  1133.58       7.0   GOOGL    1
				98  2024-08-30T00:00:00.000Z   530.70       6.10               1.15  ...   536.80     122.0    FTCO    1
				99  2024-08-30T00:00:00.000Z     5.76       0.10               1.74  ...     5.86       2.0   CURLF    1

				[100 rows x 9 columns]

			Example 2:
				# Retrieve the first 100 closed positions sorted by increasing `close_date`
				acct.get_gainloss(sort_direction='asc')
				                  close_date      cost  gain_loss  gain_loss_percent                 open_date  proceeds  quantity symbol  term
				0   2023-08-31T00:00:00.000Z   3443.90    -140.90              -4.09  2023-07-24T00:00:00.000Z   3303.00      10.0   MSFT    38
				1   2023-09-06T00:00:00.000Z  16967.00    -193.00              -1.14  2023-09-01T00:00:00.000Z  16774.00     100.0    TXN     5
				2   2023-09-06T00:00:00.000Z   5101.20      -6.70              -0.13  2023-09-06T00:00:00.000Z   5094.50      10.0   KLAC     0
				3   2023-09-06T00:00:00.000Z   5101.20       1.20               0.02  2023-09-06T00:00:00.000Z   5102.40      10.0   KLAC     0
				4   2023-09-06T00:00:00.000Z   5100.80       2.40               0.05  2023-09-06T00:00:00.000Z   5103.20      10.0   KLAC     0
				..                       ...       ...        ...                ...                       ...       ...       ...    ...   ...
				95  2024-08-20T00:00:00.000Z    122.60      -0.14              -0.11  2024-08-20T00:00:00.000Z    122.46       2.0      C     0
				96  2024-08-20T00:00:00.000Z   1886.70       4.30               0.23  2024-08-20T00:00:00.000Z   1891.00       2.0    LLY     0
				97  2024-08-20T00:00:00.000Z     45.00      -0.15              -0.33  2024-08-20T00:00:00.000Z     44.85       1.0    WMB     0
				98  2024-08-20T00:00:00.000Z    693.24      -4.24              -0.61  2024-08-20T00:00:00.000Z    689.00       2.0   SPOT     0
				99  2024-08-20T00:00:00.000Z    948.00      -0.11              -0.01  2024-08-20T00:00:00.000Z    947.89       1.0    LLY     0

				[100 rows x 9 columns]

			Example 3:
				# Retrieve all closed positions whose ticker symbol begins with `V`
				acct.get_gainloss(symbol_filter='V')
				                  close_date    cost  gain_loss  gain_loss_percent                 open_date  proceeds  quantity symbol  term
				0   2024-09-09T00:00:00.000Z  172.80       0.00               0.00  2024-08-30T00:00:00.000Z    172.80      40.0    VVR    10
				1   2024-09-09T00:00:00.000Z  121.25      15.52              12.80  2024-08-30T00:00:00.000Z    136.77      97.0    VLD    10
				2   2024-08-30T00:00:00.000Z   22.65       0.12               0.53  2024-08-29T00:00:00.000Z     22.77       3.0  VWDRY     1
				3   2024-08-30T00:00:00.000Z   45.30       0.24               0.53  2024-08-29T00:00:00.000Z     45.54       6.0  VWDRY     1
				4   2024-08-30T00:00:00.000Z   83.05       0.44               0.53  2024-08-29T00:00:00.000Z     83.49      11.0  VWDRY     1
				..                       ...     ...        ...                ...                       ...       ...       ...    ...   ...
				95  2024-08-21T00:00:00.000Z  551.76      -2.28              -0.41  2024-08-21T00:00:00.000Z    549.48     114.0    VOC     0
				96  2024-08-21T00:00:00.000Z  140.36      -0.58              -0.41  2024-08-21T00:00:00.000Z    139.78      29.0    VOC     0
				97  2024-08-21T00:00:00.000Z  121.00      -0.50              -0.41  2024-08-21T00:00:00.000Z    120.50      25.0    VOC     0
				98  2024-08-21T00:00:00.000Z   24.20      -0.10              -0.41  2024-08-21T00:00:00.000Z     24.10       5.0    VOC     0
				99  2024-08-21T00:00:00.000Z    4.84      -0.02              -0.41  2024-08-21T00:00:00.000Z      4.82       1.0    VOC     0

				[100 rows x 9 columns]

			Example 4:
				# Retrieve all positions which were closed between August 30, 2024 and September 09, 2024 [inclusive]
				acct.get_gainloss(start_date='2024-08-30', end_date='2024-09-09')
				              close_date     cost  gain_loss  gain_loss_percent                 open_date  proceeds  quantity symbol  term
				0   2024-09-09T00:00:00.000Z   172.80       0.00               0.00  2024-08-30T00:00:00.000Z    172.80      40.0    VVR    10
				1   2024-09-09T00:00:00.000Z   121.25      15.52              12.80  2024-08-30T00:00:00.000Z    136.77      97.0    VLD    10
				2   2024-09-09T00:00:00.000Z    94.14      -4.23              -4.49  2024-08-30T00:00:00.000Z     89.91       9.0    TME    10
				3   2024-09-09T00:00:00.000Z  6510.80     -39.70              -0.61  2024-08-30T00:00:00.000Z   6471.10    1985.0    SJT    10
				4   2024-09-09T00:00:00.000Z     3.50      -0.11              -3.14  2024-08-30T00:00:00.000Z      3.39      14.0   LLAP    10
				..                       ...      ...        ...                ...                       ...       ...       ...    ...   ...
				95  2024-08-30T00:00:00.000Z   530.70       6.10               1.15  2024-08-29T00:00:00.000Z    536.80     122.0   FTCO     1
				96  2024-08-30T00:00:00.000Z     5.76       0.10               1.74  2024-08-29T00:00:00.000Z      5.86       2.0  CURLF     1
				97  2024-08-30T00:00:00.000Z   315.37       2.44               0.77  2024-08-29T00:00:00.000Z    317.81      61.0    CGC     1
				98  2024-08-30T00:00:00.000Z    48.00       0.64               1.33  2024-08-29T00:00:00.000Z     48.64       8.0    ACB     1
				99  2024-08-30T00:00:00.000Z  1654.38     -13.16              -0.80  2024-08-29T00:00:00.000Z   1641.22      14.0    XOM     1

				[100 rows x 9 columns]
		'''

		#
		# Construct HTTP GET Request Parameters
		#

		params = {
			'page': page,
			'limit': limit,
			'sortBy': sort_by,
			'sort': sort_direction,
		};

		if symbol_filter is not None:
			params['symbol'] = symbol_filter.upper();

		if start_date is not None:
			params['start'] = start_date;

		if end_date is not None:
			params['end'] = end_date;

		try:
			r = requests.get(
				url = f"{self.BASE_URL}/{self.ACCOUNT_GAINLOSS_ENDPOINT}",
				params = params,
				headers = self.REQUESTS_HEADERS
			);
			r.raise_for_status();

			data = r.json();

			#
			# Validate Contents of Response from Tradier
			#

			if not data:
				print("No data received from API");
				return pd.DataFrame();

			if 'gainloss' not in data:
				print("API response missing 'gainloss'");
				print(f"Received: {r.json()}");
				return pd.DataFrame();

			if 'closed_position' not in data['gainloss']:
				print("API response missing 'closed_position'");
				print(f"Received: {r.json()}");
				return pd.DataFrame();

			closed_positions = data['gainloss']['closed_position'];
			if not closed_positions:
				print("No closed positions.");
				return pd.DataFrame();

			if isinstance(closed_positions, dict):
				closed_positions = [closed_positions];

			return pd.json_normalize(closed_positions);

		except JSONDecodeError as e:
			print(f"ERROR - JSON response decoding: {e}");
			return pd.DataFrame();
		except RequestException as e:
			print(f"ERROR - HTTP Request failed: {e}");
			return pd.DataFrame();
		except KeyError as e:
			print(f"ERROR - Unexpected API response: {e}");
			return pd.DataFrame();
		except Exception as e:
			print(f"ERROR - Unexpected garbage: {e}");
			return pd.DataFrame();

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
		try:
			r = requests.get(url='{}/{}'.format(self.BASE_URL, self.ACCOUNT_POSITIONS_ENDPOINT), params={}, headers=self.REQUESTS_HEADERS);
			r.raise_for_status();
			data = r.json();
		except requests.exceptions.RequestException as e:
			print(f"Get Positions Request Failed: {e}");
			return pd.DataFrame();
		except ValueError as e:
			print(f"JSON decode error [getPositions]: {e}");
			return pd.DataFrame();

		if data:
			if 'positions' in data:
				if 'position' in data['positions']:
					positions_df = pd.DataFrame(pd.json_normalize(data['positions']['position']));
					if symbols:
						positions_df = positions_df.query('symbol in @symbols');
					if equities:
						positions_df = positions_df[positions_df['symbol'].str.len() < 5];
						options = False;
					if options:
						positions_df = positions_df[positions_df['symbol'].str.len() > 5];
					return positions_df;
				else:
					return pd.DataFrame();
			else:
				return pd.DataFrame();
		else:
			return pd.DataFrame();