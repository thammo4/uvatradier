from .base import Tradier
import pandas as pd
import requests
import datetime
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import warnings;
from requests.exceptions import RequestException

class Quotes (Tradier):
	def __init__ (self, account_number, auth_token, live_trade=False):
		Tradier.__init__(self, account_number, auth_token, live_trade);

		#
		# Quotes endpoints for market data about equities
		#

		self.QUOTES_ENDPOINT 				= "v1/markets/quotes"; 											# GET (POST)
		self.QUOTES_HISTORICAL_ENDPOINT 	= "v1/markets/history"; 										# GET
		self.QUOTES_SEARCH_ENDPOINT 		= "v1/markets/search"; 											# GET
		self.QUOTES_TIMESALES_ENDPOINT 		= "v1/markets/timesales"; 										# GET

	def get_historical_quotes (self, symbol, interval='daily', start_date=None, end_date=None, verbose=False):
		'''
		Fetch historical OHLCV bar data for a given security's symbol from the Tradier Account API.

		Args:
			• symbol (str): The trading symbol (ticker or OCC) of the security (e.g., 'AAPL', 'MSFT', 'NKE241018P00075000').
			• interval (str, optional): The time interval for historical data. Default is 'daily'. One of: daily, weekly, monthly.
			• start_date (str 'YYYY-MM-DD', optional): The start date for historical data. Default contingent on interval argument (see Notes below).
			• end_date (str 'YYYY-MM-DD', optional): The end date for historical data. Default is current date.
			• verbose (bool, optional): Print (possibly) helpful debugging info about request parameters, api response, etc.

		Returns:
			• pandas.DataFrame: A DataFrame containing historical stock data for the specified symbol.

		Notes:
			• Default start_date values conditional upon interval argument:
				• interval='daily' 	-> start_date = most recent monday
				• interval='weekly' 	-> start_date = 12 weeks before end_date
				• interval='monthly' 	-> start_date = 1 year before end_date
			• Tradier does not maintain historical data for expired options.

		Example 1: Minimal Arguments.
			# Create a Quotes instance.
			>>> quotes = Quotes(tradier_acct, tradier_token)

			# Retrieve daily OHLCV bar data for M&T Bank for current week.
			# (Run on a Tuesday -> returns row for Monday and Tuesday)
			>>> quotes.get_historical_quotes('MTB')
			        date    open    high      low    close  volume
			0 2024-10-14  185.19  186.91  182.905  185.560  980439
			1 2024-10-15  187.08  190.23  185.280  189.905  756967

		Example 2: Weekly OHLCV data without specified dates.
			# Create a Quotes instance.
			>>> quotes = Quotes(tradier_acct, tradier_token)

			# Retrieve weekly data over past 12 weeks data for M&T Bank.
			>>> quotes.get_historical_quotes('MTB', interval='weekly')
			         date    open     high       low    close   volume
			0  2024-07-29  174.88  175.180  159.1400  162.290  4814917
			1  2024-08-05  157.93  164.420  155.1000  162.230  4275015
			2  2024-08-12  163.23  164.880  158.1850  163.090  4210555
			3  2024-08-19  163.09  170.880  161.1450  168.680  3549740
			4  2024-08-26  169.79  172.380  166.0700  170.760  3817783
			5  2024-09-02  172.17  173.285  165.1500  166.510  3855579
			6  2024-09-09  166.66  169.670  161.4000  168.880  4504412
			7  2024-09-16  169.61  180.250  168.9701  179.560  7557681
			8  2024-09-23  179.21  180.635  172.5050  175.420  5170467
			9  2024-09-30  175.48  178.970  170.1000  178.740  4891957
			10 2024-10-07  177.86  185.980  176.6700  185.190  4331667
			11 2024-10-14  185.19  190.230  182.9050  189.305  1789851

		Example 3: Retrieve monthly data for M&T Bank between April 14, 2021 and January 18, 2023.
			# Create a Quotes instance.
			>>> quotes = Quotes(tradier_acct, tradier_token)

			# Retrieve monthly data for M&T Bank.
			>>> quotes.get_historical_quotes('MTB', interval='monthly', start_date='2021-04-14', end_date='2023-01-18')
			         date    open      high      low   close    volume
			0  2021-05-01  159.30  168.2700  154.950  160.69  16054621
			1  2021-06-01  162.19  164.3900  142.550  145.31  18924640
			2  2021-07-01  147.08  147.8601  128.460  133.85  21389600
			3  2021-08-01  134.47  143.2200  131.290  140.01  17082781
			4  2021-09-01  140.31  154.7100  131.420  149.34  20531510
			5  2021-10-01  152.32  162.5400  145.720  147.12  20544524
			6  2021-11-01  149.03  163.2600  145.930  146.61  19397263
			7  2021-12-01  150.04  156.6600  141.490  153.58  18800067
			8  2022-01-01  155.77  186.9300  155.240  169.38  37110333
			9  2022-02-01  169.11  186.9500  168.100  182.23  24752575
			10 2022-03-01  179.84  186.6900  167.020  169.50  36583333
			11 2022-04-01  172.14  184.2900  157.950  166.64  42242399
			12 2022-05-01  168.25  181.1200  159.410  179.97  24896017
			13 2022-06-01  180.51  181.7900  156.190  159.39  23126308
			14 2022-07-01  158.63  178.0750  148.800  177.45  22184583
			15 2022-08-01  176.64  193.4200  173.400  181.78  17840093
			16 2022-09-01  181.76  191.3500  173.540  176.32  22113940
			17 2022-10-01  178.83  192.5600  159.395  168.37  33214286
			18 2022-11-01  169.72  172.5850  162.070  170.02  25592408
			19 2022-12-01  170.68  171.2700  138.430  145.06  31316314
			20 2023-01-01  145.00  158.0000  139.030  156.00  25906356

		Example 4: Retrieve monthly data for M&T Bank between April 14, 2021 and January 18, 2023.
			# Create a Quotes instance.
			>>> quotes = Quotes(tradier_acct, tradier_token)

			# Retrieve historical daily OHLCV bar data for option contract
			# Note - by setting the start_date to a reasonably far back past date, we obtain the prices for the entirety of the contract's life.
			# Note - this example may not work in the future because Tradier does not maintain historical data for expired options.
			>>> quotes.get_historical_quotes('MTB241115C00190000', start_date='2024-06-01')
			         date  open  high   low  close  volume
			0  2024-07-18  3.39  3.39  3.39   3.39       1
			1  2024-07-19  2.85  2.89  2.85   2.89       4
			2  2024-07-22  3.67  3.67  3.67   3.67       2
			3  2024-07-24  3.80  4.40  3.80   4.40      87
			4  2024-07-31  4.70  4.70  4.70   4.70      50
			5  2024-08-05  2.25  2.30  2.25   2.30       4
			6  2024-08-09  1.75  1.75  1.75   1.75       1
			7  2024-08-14  1.18  1.18  1.18   1.18       1
			8  2024-08-21  0.94  0.94  0.94   0.94       1
			9  2024-08-22  1.14  1.14  1.14   1.14       1
			10 2024-08-28  1.75  1.85  1.75   1.85       2
			11 2024-09-03  2.65  2.65  2.65   2.65       2
			12 2024-09-05  2.30  2.30  2.30   2.30      36
			13 2024-09-06  1.75  1.75  1.75   1.75      35
			14 2024-09-11  1.30  1.30  1.30   1.30       2
			15 2024-09-16  2.15  2.30  2.15   2.30      65
			16 2024-09-17  2.75  2.75  2.75   2.75       1
			17 2024-09-18  3.08  3.08  3.08   3.08      10
			18 2024-09-19  3.90  3.90  3.90   3.90      10
			19 2024-09-20  3.45  3.80  3.45   3.80      10
			20 2024-09-23  3.20  3.20  3.20   3.20      16
			21 2024-09-24  3.50  3.50  3.50   3.50      34
			22 2024-09-25  2.22  2.22  2.22   2.22       1
			23 2024-09-30  3.90  3.90  3.90   3.90       1
			24 2024-10-01  2.64  2.67  2.64   2.67       2
			25 2024-10-02  2.25  2.29  2.20   2.20      31
			26 2024-10-03  2.00  2.00  2.00   2.00       3
			27 2024-10-07  3.67  3.67  3.67   3.67       1
			28 2024-10-08  3.40  3.60  3.40   3.60      31
			29 2024-10-09  3.37  3.37  3.37   3.37       1
			30 2024-10-10  3.17  3.17  3.17   3.17       1
			31 2024-10-11  5.82  6.00  5.35   5.84      63
			32 2024-10-14  5.80  5.92  5.62   5.92      26
			33 2024-10-15  6.70  8.10  6.70   8.00      54
		'''

		#
		# Ensure that provided symbol is a string in uppercase format
		#

		if not isinstance(symbol, str):
			print(f"Symbol argument must be a string. Received: ({symbol}, {type(symbol)})");
			return pd.DataFrame();

		symbol = symbol.upper();

		#
		# Check that the interval is legit (daily, weekly, monthly)
		#

		if not isinstance(interval, str):
			print(f"Interval must be string. One of: daily, weekly, monthly");
			return pd.DataFrame();

		interval = interval.lower();
		if interval not in ['daily', 'weekly', 'monthly']:
			print(f"Invalid interval. One of: daily, weekly, monthly");
			return pd.DataFrame();

		#
		# Helper function used to index the start of the trading week
		#

		def last_monday (input_date):
			''' Hand over last Monday's date '''
			if input_date.weekday() == 0:
				return input_date - timedelta(days=7);
			else:
				return input_date - timedelta(days=input_date.weekday());

		#
		# Infer the appropriate start/end dates (per interval) if not supplied by user
		# 	• if end_date not supplied -> end_date set to current date
		#	• if start_date not supplied:
		# 		• interval='daily' 		-> start_date = most recent monday
		# 		• interval='weekly' 	-> start_date = 12 weeks ago
		# 		• interval='monthly' 	-> start_date = last year
		#

		if end_date is None:
			end_date = datetime.today().strftime("%Y-%m-%d");

		if start_date is None:
			if interval == 'monthly':
				tmp_dt = (datetime.strptime(end_date, '%Y-%m-%d')-timedelta(weeks=52)).replace(day=1);
			elif interval == 'weekly':
				tmp_dt = (datetime.strptime(end_date, '%Y-%m-%d')-timedelta(weeks=12));
			else:
				tmp_dt = last_monday(datetime.strptime(end_date, '%Y-%m-%d'));

			start_date = tmp_dt.strftime('%Y-%m-%d');

		try:
			if verbose:
				print("Sending HTTP GET Request...");
				print(f"HTTP Request Params: (symbol={symbol}, interval={interval}, start={start_date}, end={end_date})\n");

			#
			# HTTP GET Request
			#

			r = requests.get(
				url  	= f"{self.BASE_URL}/{self.QUOTES_HISTORICAL_ENDPOINT}",
				params 	= {'symbol':symbol, 'interval':interval, 'start':start_date, 'end':end_date},
				headers = self.REQUESTS_HEADERS
			);
			r.raise_for_status();

			data = r.json();

			if verbose:
				print(f"DATA:\n{data}\n");

			#
			# Validate the structure of the API Response from Tradier
			#

			if not data:
				raise ValueError(f"Empty API Response. Status Code: {r.status_code}");
			if 'history' not in data:
				raise KeyError(f"API response missing 'history'. Received: {data}");
			if data['history'] is None:
				raise ValueError(f"No historical data for (symbol={symbol}, start_date={start_date}, end_date={end_date})");
			if 'day' not in data['history']:
				raise KeyError(f"API Response history data missing 'day': {data}");


			#
			# Extract the sought information from the API response and prepare returned dataframe
			#

			df = pd.json_normalize(data['history']['day']);
			df['date'] = pd.to_datetime(df['date']);

			if verbose:
				print(f"Returning Structure:\n{df.info()}\n");

			#
			# Off you go!
			#

			return df;

		except (requests.exceptions.RequestException, ValueError, KeyError) as e:
			raise RuntimeError(f"[Historical Quotes] ... {e}");


	def get_quote_day (self, symbol, last_price=False):
		'''
		Fetch the current quote data for a given symbol from the Tradier Account API.

		Args:
			• symbol (str): The trading symbol of the stock (e.g., 'AAPL', 'MSFT') for which you want to retrieve the current quote data.
			• last_price (bool, optional): If True, only fetch the last price of the symbol. Default is False.

		Returns:
			• pandas.DataFrame or float: A DataFrame containing the current quote data for the specified symbol or just the last price as a float if last_price is set to True.

		Example:
			# Create a Quotes instance
			quotes = Quotes(tradier_acct, tradier_token)

			# Retrieve current quote data for symbol 'CCL' and transpose the DataFrame for easy viewing
			ccl_quote = quotes.get_quote_day(symbol='CCL').T

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
			last_price = quotes.get_quote_day(symbol='CCL', last_price=True)
			Sample Output: 15.73
		'''

		if not isinstance(symbol, str):
			quote_columns = ['symbol', 'description', 'exch', 'type', 'last', 'change', 'volume', 'open', 'high', 'low', 'close', 'bid', 'ask', 'change_percentage', 'average_volume', 'last_volume', 'trade_date', 'prevclose', 'week_52_high', 'week_52_low', 'bidsize', 'bidexch', 'bid_date', 'asksize', 'askexch', 'ask_date', 'root_symbols'];
			return pd.DataFrame({col:[] for col in quote_columns});

		symbol = symbol.upper();

		try:

			r = requests.get(
				url 	= f"{self.BASE_URL}/{self.QUOTES_ENDPOINT}",
				params 	= {'symbols':symbol, 'greeks':'false'},
				headers = self.REQUESTS_HEADERS
			);
			r.raise_for_status();

			quote_json = r.json();
			if quote_json is None or 'quotes' not in quote_json:
				print('API Response Lacks quotes key.');
				return pd.DataFrame();

			quote_dict = quote_json['quotes'];
			if quote_dict is None or 'quote' not in quote_dict:
				print(f'No quote data for: {symbol}.');
				return pd.DataFrame();

			quote_data = quote_dict['quote'];

			df_quote = pd.json_normalize(quote_data);

			if last_price:
				if not isinstance(last_price, bool):
					print("YO! ... Second argument 'last_price' should be bool.");
				if 'last' not in df_quote:
					return f"No last price found: {symbol}.";
				return float(df_quote['last'].iloc[0]);

			return df_quote;

		except requests.exceptions.RequestException as e:
			return f"API Request Failed: {str(e)}.";
		except ValueError as e:
			return f"API Response Parse Error: {str(e)}.";
		except KeyError as e:
			return f"Unexpected API Response Structure: {str(e)}.";
		except Exception as e:
			return f"Something has gone terribly wrong: {str(e)}";

	def get_quote_data (self, symbol_list):
		'''
		Retrieve a dataframe with current quote data for a specified list of stock symbols.
		The returned DataFrame can be used to quickly compare properties of different stocks side-by-side.

		Args:
			• symbol (list):
				• List whose elements are strings that denote the desired symbol ['ONE', 'TWO', 'ETC']

		Returns:
			• pandas.DataFrame:
				• (DF) A DataFrame containing the current quote data for the specified symbol list.

		Example:
			# Create a Quotes instance
			quotes = Quotes(tradier_acct, tradier_token)

			# Retrieve current quote data for Citi Group, JP Morgan, and Goldman Sachs
			quotes.get_quote_data(symbol_list=['C', 'JPM', 'GS'])

			Sample Output: (transposed to show full field list)
			                               0                    1                            2
			symbol                         C                  JPM                           GS
			description        Citigroup Inc  JPMorgan Chase & Co  The Goldman Sachs Group Inc
			exch                           N                    N                            N
			type                       stock                stock                        stock
			last                      65.605               207.75                     478.7975
			change                     -1.38                -0.05                         -0.1
			volume                  13189182              6467719                      1349715
			open                      66.185               206.21                        480.0
			high                        66.5                208.1                       483.16
			low                       65.305               205.38                       476.27
			close                       None                 None                         None
			bid                         65.6               207.74                       478.66
			ask                        65.61               207.76                       478.93
			change_percentage          -2.06                -0.03                        -0.02
			average_volume          19151906             10767333                      2817983
			last_volume                  100                  100                          100
			trade_date         1720726003419        1720726004190                1720725986965
			prevclose                  66.98                207.8                       478.89
			week_52_high               66.99               210.38                       479.86
			week_52_low                38.17               135.19                     289.3568
			bidsize                       17                    1                            1
			bidexch                        Q                    P                            Z
			bid_date           1720725998000        1720726003000                1720726003000
			asksize                        8                    2                            2
			askexch                        N                    Q                            M
			ask_date           1720726003000        1720726001000                1720726001000
			root_symbols                   C                  JPM                       GS,GS1
		'''

		#
		# Sanity check
		#

		if not symbol_list or symbol_list is None:
			print('Nothing given nothing gained.');
			return pd.DataFrame();

		#
		# For convenience, we'll just convert the singular case to a list
		#

		if isinstance(symbol_list, str):
			symbol_list = [symbol_list];

		#
		# Check that the user didn't provide junk symbols
		#

		valid_symbols = [];
		for s in symbol_list:
			if not isinstance(s, str):
				print(f"symbols only 'round these parts: {s} ({type(s)})");
			else:
				valid_symbols.append(s.upper());

		str_symbols = ",".join(valid_symbols);

		if not str_symbols:
			print("No ticker symbols?");
			return pd.DataFrame();

		try:
			r = requests.get(
				url = f"{self.BASE_URL}/{self.QUOTES_ENDPOINT}",
				params = {"symbols":str_symbols, "greeks":"false"},
				headers = self.REQUESTS_HEADERS
			);
			r.raise_for_status();

			quotes_json = r.json();

			if quotes_json is None or 'quotes' not in quotes_json:
				print("API Response Error [1]: No 'quotes' key");
				print(quotes_json);
				return pd.DataFrame();

			quotes_dict = quotes_json['quotes'];

			if quotes_dict is None or 'quote' not in quotes_dict:
				print("API Response Error [2]: No 'quote' key");
				print(quotes_dict);
				return pd.DataFrame();

			quotes_data = quotes_dict['quote'];

			if not quotes_data:
				print('No quotes data.');
				quotes_df = pd.DataFrame();
			else:
				quotes_df = pd.json_normalize(quotes_data);

			return quotes_df;

		except requests.exceptions.RequestException as e:
			print(f'Failed API Request: {str(e)}.');
			return pd.DataFrame();
		except ValueError as e:
			print(f"API Response Parse Issue: {str(e)}.");
			return pd.DataFrame();
		except KeyError as e:
			print(f"Unexpected API response: {str(e)}.");
			return pd.DataFrame();
		except Exception as e:
			print(f"Something terrible as happened: {str(e)}.");
			pd.DataFrame();

	def get_timesales (self, symbol, interval='1min', start_time=None, end_time=None):
		'''
		Retrieve intraday OHLCV bar data for a given stock at a specified time interval.

		Args:
			• symbol (str): The trading symbol of the stock (e.g., 'AAPL', 'MSFT') for which you want to retrieve intraday data.
			• interval (str, optional): The time interval for intraday data. Default is '1min'. One of: tick, 1min, 5min, 15min.
			• start_time (str 'YYYY-MM-DD HH:MM', optional): The start time for the intraday data returned. This will be the first row of the result set.
			• end_date (str 'YYYY-MM-DD HH:MM', optional): The end time for the intraday data returned.

		Returns:
			• pandas.DataFrame: A DataFrame containing intraday OHLCV bar data for the specified symbol.

		Notes:
			• Tradier does not keep past intraday data available indefinitely. This should be used primarily for very recent dates. To test with the below examples, adjust the date to something closer to the current date. For more, see:

				https://documentation.tradier.com/brokerage-api/markets/get-timesales

		Example 1: Minimal Arguments
			# Create a Quotes instance
			>>> quotes = Quotes(tradier_acct, tradier_token)

			# Retrieve intraday stock data for symbol Citi (C)
			>>> quotes.get_timesales("C")
			                   time   timestamp     price     open     high      low    close   volume       vwap
			0   2024-10-04T16:00:00  1728072000  62.64000  62.6400  62.6400  62.6400  62.6400  1618854  62.640000
			1   2024-10-04T16:06:00  1728072360  62.64000  62.6400  62.6400  62.6400  62.6400     2651  62.640000
			2   2024-10-04T16:08:00  1728072480  62.64000  62.6400  62.6400  62.6400  62.6400      565  62.640000
			3   2024-10-04T16:24:00  1728073440  62.51000  62.5100  62.5100  62.5100  62.5100      400  62.510000
			4   2024-10-04T16:26:00  1728073560  62.51010  62.5101  62.5101  62.5101  62.5101      116  62.527989
			5   2024-10-04T16:31:00  1728073860  62.52500  62.5200  62.5400  62.5100  62.5100     2880  62.515042
			6   2024-10-04T16:36:00  1728074160  62.64000  62.6400  62.6400  62.6400  62.6400   123816  62.640000
			7   2024-10-04T16:58:00  1728075480  62.64000  62.6400  62.6400  62.6400  62.6400    96911  62.640000
			8   2024-10-04T16:59:00  1728075540  62.52000  62.5200  62.5200  62.5200  62.5200      300  62.520000
			9   2024-10-04T17:07:00  1728076020  62.58000  62.5800  62.5800  62.5800  62.5800      150  62.580000
			10  2024-10-04T17:17:00  1728076620  62.57500  62.5700  62.5800  62.5700  62.5800      479  62.573027
			11  2024-10-04T17:27:00  1728077220  62.57000  62.5700  62.5700  62.5700  62.5700      700  62.570000
			12  2024-10-04T17:41:00  1728078060  62.57000  62.5700  62.5700  62.5700  62.5700      400  62.570000
			13  2024-10-04T17:42:00  1728078120  62.56000  62.5600  62.5600  62.5600  62.5600     1000  62.559600
			14  2024-10-04T18:36:00  1728081360  62.57000  62.5700  62.5700  62.5700  62.5700      200  62.570000
			15  2024-10-04T18:42:00  1728081720  62.57925  62.5700  62.5885  62.5700  62.5885      600  62.579025
			16  2024-10-04T18:43:00  1728081780  62.58500  62.5900  62.5900  62.5800  62.5800      200  62.585000
			17  2024-10-04T18:53:00  1728082380  62.57500  62.5800  62.5800  62.5700  62.5700      241  62.575851
			18  2024-10-04T18:59:00  1728082740  62.59000  62.5900  62.5900  62.5900  62.5900      100  62.590000
			19  2024-10-04T19:33:00  1728084780  62.50110  62.5011  62.5011  62.5011  62.5011      352  62.503462
			20  2024-10-04T19:56:00  1728086160  62.53000  62.5300  62.5300  62.5300  62.5300      500  62.530000

		Example 2: Weyerhauser 15-minute interval intraday data for afternoon of October 4, 2024.
			# Create a Quotes instance
			>>> quotes = Quotes(tradier_acct, tradier_token)

			# Retrieve intraday Weyerhauser data.
			>>> quotes.get_timesales(symbol='WY', interval='15min', start_time='2024-10-04 12:00', end_time='2024-10-04 16:00')
			                   time   timestamp     price    open     high     low   close  volume       vwap
			0   2024-10-04T12:00:00  1728057600  32.82250  32.805  32.8850  32.760  32.800  112648  32.831508
			1   2024-10-04T12:15:00  1728058500  32.78750  32.808  32.8350  32.740  32.765   38523  32.783795
			2   2024-10-04T12:30:00  1728059400  32.84000  32.770  32.9150  32.765  32.900   37764  32.837720
			3   2024-10-04T12:45:00  1728060300  32.94250  32.900  32.9950  32.890  32.965   80334  32.954177
			4   2024-10-04T13:00:00  1728061200  33.00250  32.965  33.0500  32.955  33.005   60547  33.008234
			5   2024-10-04T13:15:00  1728062100  32.98250  33.010  33.0150  32.950  32.955   37137  32.996037
			6   2024-10-04T13:30:00  1728063000  32.96250  32.950  33.0150  32.910  33.000   41859  32.969801
			7   2024-10-04T13:45:00  1728063900  32.94945  33.000  33.0089  32.890  32.910   30530  32.942807
			8   2024-10-04T14:00:00  1728064800  32.89000  32.910  32.9150  32.865  32.900   86852  32.889426
			9   2024-10-04T14:15:00  1728065700  32.91750  32.900  32.9600  32.875  32.930   31357  32.918224
			10  2024-10-04T14:30:00  1728066600  32.93750  32.930  32.9650  32.910  32.940   24714  32.942706
			11  2024-10-04T14:45:00  1728067500  32.95500  32.945  32.9750  32.935  32.955   43628  32.957438
			12  2024-10-04T15:00:00  1728068400  32.95250  32.950  33.0000  32.905  32.985   65831  32.957778
			13  2024-10-04T15:15:00  1728069300  32.99000  32.990  33.0250  32.955  32.965   78064  32.998393
			14  2024-10-04T15:30:00  1728070200  32.98000  32.965  33.0100  32.950  33.005   79725  32.983402
			15  2024-10-04T15:45:00  1728071100  32.93750  33.005  33.0050  32.870  32.880  589946  32.935760
			16  2024-10-04T16:00:00  1728072000  32.88000  32.880  32.8800  32.880  32.880  928888  32.880000
		'''

		#
		# Confirm symbol argument
		#

		if not symbol:
			raise ValueError("No ticker provided.");
			return pd.DataFrame();

		symbol = symbol.upper();

		#
		# Check for valid interval
		#

		valid_intervals = ['tick', '1min', '5min', '15min'];
		if interval not in valid_intervals:
			raise ValueError(f"Invalid Interval. Valid: {', '.join(valid_intervals)}");
			return pd.DataFrame();

		r_params = {'symbol':symbol, 'interval':interval};
		if start_time is not None:
			r_params['start'] = start_time;
		if end_time is not None:
			r_params['end'] = end_time;

		try:
			r = requests.get(
				url = f"{self.BASE_URL}/{self.QUOTES_TIMESALES_ENDPOINT}",
				params = r_params,
				headers = self.REQUESTS_HEADERS
			);
			r.raise_for_status();

			data = r.json();

			if 'series' not in data or 'data' not in data['series']:
				raise KeyError('ERROR - API Response Missing Data.');
				return pd.DataFrame();

			return pd.json_normalize(r.json()['series']['data']);

		except RequestException as e:
			raise RequestException(f"ERROR - API Request: {str(e)}");
		except KeyError as e:
			raise KeyError(f"ERROR - API Response Parse: {str(e)}");
		except Exception as e:
			raise Exception(f"ERROR - Unexpected API Response: {str(e)}");

	def get_timeseries_plot (self, symbol, plot_var='close', interval='daily', start_date=False, end_date=False):
		'''
			Construct a time series plot of the dataframe returned by Quotes.get_historical_quotes.

			Args:
				plot_var (str): lowercase string indicating the bar-data column to put onto the plot ['open', 'high', 'low', 'close', 'volume']

			See help(Quotes.get_historical_quotes) for information about remaining parameters.
		'''
		bar_data = self.get_historical_quotes(symbol, interval, start_date, end_date);
		bar_data['date'] = pd.to_datetime(bar_data['date']);
		bar_data.set_index('date', inplace=True);
		plot_str = "{} {} Price".format(symbol.upper(), plot_var[0].upper() + plot_var[1:]);
		plt.plot(bar_data[plot_var], label=plot_str);
		plt.title(plot_str);
		plt.legend();
		plt.show();

	def search_companies (self, query):
		if not query:
			return "Need that search term yo";

		r = requests.get(
			url = '{}/{}'.format(self.BASE_URL, self.QUOTES_SEARCH_ENDPOINT),
			params = {'q': query, 'indexes':'false'},
			headers = self.REQUESTS_HEADERS
		);

		if not r.json()['securities']:
			return "Nothing found";

		return pd.DataFrame(r.json()['securities']['security']);
