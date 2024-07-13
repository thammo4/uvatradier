from .base import Tradier
import pandas as pd
import requests
import datetime
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import warnings;

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

	def get_historical_quotes (self, symbol, interval='daily', start_date=False, end_date=False, verbose=False):

		'''
		Fetch historical stock data for a given symbol from the Tradier Account API.

		This function makes a GET request to the Tradier Account API to retrieve historical stock
		data for a specified symbol within a specified time interval.

		Args:
			symbol (str): The trading symbol of the stock (e.g., 'AAPL', 'MSFT') for which you want
			              to retrieve historical data.
			interval (str, optional): The time interval for historical data. Default is 'daily'. Alt values are 'weekly' or 'monthly'.
			start_date (str, optional): The start date for historical data in the format 'YYYY-MM-DD'.
			                           If not provided, the function will default to the most recent Monday.
			end_date (str, optional): The end date for historical data in the format 'YYYY-MM-DD'.
			                         If not provided, the function will default to the current date.

		Returns:
			pandas.DataFrame: A DataFrame containing historical stock data for the specified symbol.

		Example:
			# Create a Quotes instance
			quotes = Quotes(ACCOUNT_NUMBER, AUTH_TOKEN)

			# Retrieve historical stock data for symbol 'BIIB'
			historical_data = quotes.get_historical_quotes(symbol='BIIB')

			Sample Output:
			         date    open     high     low   close   volume
			0  2023-08-28  265.40  266.470  263.54  265.05   359872
			1  2023-08-29  265.35  268.150  265.11  268.00   524972
			2  2023-08-30  268.84  269.460  265.25  267.18   552728
			3  2023-08-31  266.83  269.175  265.32  267.36  1012842
			4  2023-09-01  269.01  269.720  266.91  267.17   522401
		'''

		#
		# Ensure that provided symbol is in uppercase format
		#

		if not symbol:
			return 'No ticker symbol provided.';

		symbol = symbol.upper();

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

		try:

			r = requests.get(
				url 	= '{}/{}'.format(self.BASE_URL, self.QUOTES_HISTORICAL_ENDPOINT),
				params 	= {
					'symbol' 	: symbol,
					'interval' 	: interval,
					'start' 	: start_date,
					'end' 		: end_date
				},
				headers = self.REQUESTS_HEADERS
			);
			r.raise_for_status();

		except requests.exceptions.RequestException as e:
			return f"Request failed: {e}";

		try:
			data = r.json();
		except ValueError as e:
			return f"JSON decode issue: {str(e)}.\nResponse content: {r.text[:500]}";

		if verbose:
			print(f'DATA:\n{data}');

		if not data:
			return f"Empty response from API: {r.status_code}.";

		if 'history' not in data:
			return f"Unexpected API garb [history not in data]: {data}";

		if data['history'] is None:
			return f"Historical data returned 'None': ({symbol}, {start_date}, {end_date})";

		if 'day' not in data['history']:
			return f"No day in history data: {data['history']}.";

		if 'history' not in data or 'day' not in data['history']:
			return 'Unexpected API response.'

		return pd.DataFrame(data['history']['day']);

	def get_quote_day (self, symbol, last_price=False):
		'''
		Fetch the current quote data for a given symbol from the Tradier Account API.

		This function makes a GET request to the Tradier Market Data API to retrieve the current quote
		data for a specified symbol.

		Args:
			symbol (str): The trading symbol of the stock (e.g., 'AAPL', 'MSFT') for which you want
			              to retrieve the current quote data.
			last_price (bool, optional): If True, only fetch the last price of the symbol. Default is False.

		Returns:
			pandas.DataFrame or float: A DataFrame containing the current quote data for the specified symbol
									   or just the last price as a float if last_price is set to True.

		Example:
			# Create a Quotes instance
			quotes = Quotes(ACCOUNT_NUMBER, AUTH_TOKEN)

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
			return "Symbol needs to be a string (duh?)";

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
				return float(df_quote['last']);

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
			quotes = Quotes(ACCOUNT_NUMBER, AUTH_TOKEN)

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

	def get_timesales (self, symbol, interval='1min', start_time=False, end_time=False):
		'''
			This function returns the tick data for `symbol` in increments specified by `interval`.
			Eventually, we can use this to analyze/visualze stock data in a time series context.

			Arguments `start_time` and `end_time` must be strings with format 'YYYY-MM-DD HH:MM'

			Sample output:
				>>> quotes.get_timesales('VZ', start_time='2023-09-27 09:45', end_time='2023-09-27 14:00')
				                    time   timestamp     price     open     high      low   close  volume       vwap
				0    2023-09-27T09:45:00  1695822300  32.92995  32.9500  32.9500  32.9099  32.915   39077  32.924828
				1    2023-09-27T09:46:00  1695822360  32.89560  32.9112  32.9112  32.8800  32.895   32867  32.891113
				2    2023-09-27T09:47:00  1695822420  32.88750  32.8950  32.9100  32.8650  32.910   75720  32.888736
				3    2023-09-27T09:48:00  1695822480  32.91750  32.9100  32.9250  32.9100  32.910   15126  32.913109
				4    2023-09-27T09:49:00  1695822540  32.91000  32.9100  32.9200  32.9000  32.920   20335  32.907385
				..                   ...         ...       ...      ...      ...      ...     ...     ...        ...
				251  2023-09-27T13:56:00  1695837360  32.35425  32.3450  32.3655  32.3430  32.360   58256  32.354522
				252  2023-09-27T13:57:00  1695837420  32.35500  32.3500  32.3600  32.3500  32.360   15825  32.355307
				253  2023-09-27T13:58:00  1695837480  32.36125  32.3599  32.3700  32.3525  32.365   34624  32.362786
				254  2023-09-27T13:59:00  1695837540  32.37500  32.3700  32.3900  32.3600  32.390   27728  32.370699
				255  2023-09-27T14:00:00  1695837600  32.38750  32.3866  32.3950  32.3800  32.385   53837  32.386281

				(vwap = volume weighted average price during the interval)
		'''

		if not symbol:
			return 'No ticker symbol provided';

		symbol = symbol.upper();


		r_params = {'symbol':symbol};
		if start_time:
			r_params['start'] = start_time;
		if end_time:
			r_params['end'] = end_time;

		r = requests.get(
			url = '{}/{}'.format(self.BASE_URL, self.QUOTES_TIMESALES_ENDPOINT),
			params = r_params,
			headers = self.REQUESTS_HEADERS
		);

		return pd.json_normalize(r.json()['series']['data']);

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