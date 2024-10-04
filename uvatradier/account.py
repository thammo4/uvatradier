import requests
import pandas as pd
from requests.exceptions import RequestException, JSONDecodeError;

from .base import Tradier

class Account (Tradier):
	def __init__ (self, account_number, auth_token, live_trade=False):
		Tradier.__init__(self, account_number, auth_token, live_trade);
		
		#
		# Account endpoints
		#

		self.PROFILE_ENDPOINT = "v1/user/profile"; 													# GET

		self.POSITIONS_ENDPOINT = f"v1/accounts/{account_number}/positions";  						# GET

		self.ACCOUNT_BALANCE_ENDPOINT  	= f"v1/accounts/{account_number}/balances"; 	 			# GET
		self.ACCOUNT_GAINLOSS_ENDPOINT 	= f"v1/accounts/{account_number}/gainloss"; 		 		# GET
		self.ACCOUNT_HISTORY_ENDPOINT 	= f"v1/accounts/{account_number}/history"; 			 		# GET
		self.ACCOUNT_POSITIONS_ENDPOINT = f"v1/accounts/{account_number}/positions"; 		 		# GET

		self.ORDER_ENDPOINT = f"v1/accounts/{account_number}/orders"; 					 			# GET

	def get_user_profile (self, is_sole_account=False):
		'''
		Fetch the user profile's account information from the Tradier Account API.

		This function makes a GET request to the Tradier Account API. For each account associated with your profile, it provides basic information
		such as created/last-updated dates, option trading level, account's margin status, etc...

		Args (Optional):
			• is_sole_account (bool): If you only have 1 account with Tradier under your profile, and you want your account info in a Pandas Series instead of the first (and what would be, in this case, the only) row of a DataFrame.

		Returns:
		    • pandas.DataFrame: A DataFrame containing user profile information.

		Notes:
		    • For profiles having n-accounts, n ≥ 2, each account will be a row in the returned DataFrame. ***
		    *** (i'm pretty sure this is true, but as I've only 1 account to my name right now, I can't actually test to confirm yet.) ***

		Example:
		    # Create `Account` object with account number and authorization token credentials.
		    >>> acct = Account(tradier_acct, tradier_token)

		    # Return information about account(s) as row(s) in DataFrame.
		    >>> acct.get_user_profile()
		                     id            name account.account_number account.classification      account.date_created  account.day_trader  account.option_level account.status account.type  account.last_update_date
		    0  id-sb-3a13swkrbv  Harry Christopher Caray             VA44632119             individual  2021-06-23T22:04:20.000Z               False                     6         active       margin  2021-06-23T22:04:20.000Z

		    # Return account information as Series.
		    >>> acct.get_user_profile(True)
		    id                                  id-sb-3a13swkrbv
		    name                         Harry Christopher Caray
		    account.account_number                    VA44632119
		    account.classification                    individual
		    account.date_created        2021-06-23T22:04:20.000Z
		    account.day_trader                             False
		    account.option_level                               6
		    account.status                                active
		    account.type                                  margin
		    account.last_update_date    2021-06-23T22:04:20.000Z
		    Name: 0, dtype: object
		'''

		try:
			r = requests.get(
				url 	= f"{self.BASE_URL}/{self.PROFILE_ENDPOINT}",
				params 	= {},
				headers = self.REQUESTS_HEADERS
			);

			# We good?
			r.raise_for_status();

			if 'profile' not in r.json():
				raise KeyError("API response missing 'profile'");

			return pd.json_normalize(r.json()['profile']) if not is_sole_account else pd.json_normalize(r.json()['profile']).iloc[0];

		except requests.exceptions.RequestException as e:
			print(f"ERROR [garbage request, get_user_profile] -> {e}");
			return pd.DataFrame() if not is_sole_account else pd.Series();

		except KeyError as e:
			print(f"ERROR: [key drama, get_user_profile] -> {e}");
			return pd.DataFrame() if not is_sole_account else pd.Series();

	def get_account_balance (self, return_as_series=False):
		'''
		Fetch the account balance information from the Tradier Account API.

		This function makes a GET request to the Tradier Account API. It returns current balance information for the account associated with the account number argument provided.
		This includes cash balances, open/close P&L, short/long equity/options positions, margin info, etc... (see example below for full field list returned).

		Args (Optional):
			• return_as_series (bool, default=False): If True is passed, the function will return the account balance data in a Pandas Series object. Otherwise, it returns a DataFrame.

		Returns:
		    • (default) If return_as_series = False -> returns single row Pandas DataFrame with account balance fields denoted in the columns.
		    • If return_as_series = True -> returns Pandas Series.

		Notes:
			• There are several fields related to each account's margin (fed_call, maintenance_call, option/stock_buying_power, stock_short_value, sweep).
				• If DataFrame returned -> each margin-field will be a column of the one row dataframe.
				• If Seires returned -> there will be a 'margin' index label whose value is a dictionary containing margin-field labels/values.

		Example:
		    # Initialize Account object
		    >>> acct = Account(tradier_acct, tradier_token)

		    # Retrieve account balance info as DataFrame
		    >>> acct.get_account_balance()
		       option_short_value  total_equity account_number account_type  close_pl  current_requirement  ...  margin.fed_call  margin.maintenance_call  margin.option_buying_power  margin.stock_buying_power  margin.stock_short_value  margin.sweep
		    0             -5874.0   163905.3018     VA44632119       margin         0            141960.75  ...                0                        0                  12527.8018                 25055.6036                         0             0
		    [1 rows x 24 columns]

		    # Retrieve account balance info as Series
			>>> acct.get_account_balance(True)
			option_short_value                                                -5874.0
			total_equity                                                  163905.3018
			account_number                                                 VA44632119
			account_type                                                       margin
			close_pl                                                                0
			current_requirement                                             141960.75
			equity                                                                  0
			long_market_value                                                   232.0
			market_value                                                      -5642.0
			open_pl                                                             334.0
			option_long_value                                                       0
			option_requirement                                               159353.5
			pending_orders_count                                                    0
			short_market_value                                                -5874.0
			stock_long_value                                                    232.0
			total_cash                                                    169547.3018
			uncleared_funds                                                         0
			pending_cash                                                            0
			margin                  {'fed_call': 0, 'maintenance_call': 0, 'option...
			dtype: object
		'''

		try:
			r = requests.get(
				url = f"{self.BASE_URL}/{self.ACCOUNT_BALANCE_ENDPOINT}",
				params = {},
				headers = self.REQUESTS_HEADERS
			);

			# We good?
			r.raise_for_status();

			if 'balances' not in r.json():
				raise KeyError("API response missing 'balances'");

			return pd.json_normalize(r.json()['balances']) if not return_as_series else pd.Series(r.json()['balances']);

		except requests.exceptions.RequestException as e:
			print(f"ERROR [bad request, f(x) = Account.get_account_balance] -> {e}");
			return pd.DataFrame() if not return_as_series else pd.Series();
		except KeyError as e:
			print(f"ERROR [bad key, f(x) = Account.get_user_profile] -> {e}");
			return pd.DataFrame() if not return_as_series else pd.Series();

	def get_gainloss (self, page=1, limit=100, sort_by='closeDate', sort_direction='desc', start_date=None, end_date=None, symbol_filter=None):
		'''
		Args (All Optional):
			• page (int): Page from which to begin returning records.
			• limit (int): Number of records to return on each page.
			• sort_by (str): Field by which results will be sorted. One of: 'openDate', 'closeDate'
			• sort_dire//ction (str): Direction in which the `sortBy` field will be sorted. One of: 'asc', 'desc'.
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
				url 	= f"{self.BASE_URL}/{self.ACCOUNT_GAINLOSS_ENDPOINT}",
				params 	= params,
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
		Retrieve orders recently submitted to Tradier. Provides information related to:
			• Basic Order Info - symbol, trade, side, #shares, fill status.
			• Order Fill Metrics - mean/last fill price, #shares filled/to-be-filled.
			• (Options Only) options strategy inferred from legs of trade, OCC symbols comprising combination position.

		Returns:
		    • pandas.DataFrame: Each row is a (potentially multileg) options or equity order submitted.

		Example:
		    # Create `Account` object with account number and authorization token credentials.
		    >>> acct = Account(tradier_acct, tradier_token)

		    # Retrieve orders that were recently submitted (shown: 2 credit spread orders)
		    >>> acct.get_orders()
			         id    type symbol side  quantity  status duration  avg_fill_price  ...  last_fill_quantity  remaining_quantity               create_date          transaction_date     class num_legs strategy                                                leg
			0  14327159  market    AON  buy       2.0  filled      day           -2.40  ...                 1.0                 0.0  2024-10-03T16:59:11.262Z  2024-10-03T16:59:11.537Z  multileg        2   spread  [{'id': 14327160, 'type': 'market', 'symbol': ...
			1  14327360  market    DRI  buy       2.0  filled      day           -0.05  ...                 1.0                 0.0  2024-10-03T17:09:22.613Z  2024-10-03T17:09:22.853Z  multileg        2   spread  [{'id': 14327361, 'type': 'market', 'symbol': ...

			[2 rows x 18 columns]
		'''

		r = requests.get(
			url 	= f"{self.BASE_URL}/{self.ORDER_ENDPOINT}",
			params 	= {'includeTags':'true'},
			headers = self.REQUESTS_HEADERS
		);

		if r.json()['orders'] == 'null':
			print('You have no current orders.')
			return pd.DataFrame();

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
										matching these symbols will be included. Exact matches only are returned.
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
			r = requests.get(
				url 	= f"{self.BASE_URL}/{self.ACCOUNT_POSITIONS_ENDPOINT}",
				params 	= {},
				headers = self.REQUESTS_HEADERS
			);
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