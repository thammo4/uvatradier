from .base import Tradier

import requests
import pandas as pd

class OptionsData (Tradier):
	def __init__ (self, account_number, auth_token, live_trade=False):
		Tradier.__init__(self, account_number, auth_token, live_trade);

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
			url 	= '{}/{}'.format(self.BASE_URL, self.OPTIONS_CHAIN_ENDPOINT),
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
			url 	= '{}/{}'.format(self.BASE_URL, self.OPTIONS_EXPIRY_ENDPOINT),
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

	# ##########################
	# TODO (9/27):
	# 		1. Change get_options_symbols so that it returns the dataframe format by default
	# 		2. Investigate the KeyError: 'expiration_date' error produced from `options.get_options_symbols('BWA', df=True)`
	# 			• Issue arises because there are two different symbols for BorgWarner Inc. {'BWA', 'BWA1'}
	# 			• Not sure how to fix this problem yet though
	# ##########################

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
					parsed_options.append({'symbol':option,'root_symbol':root_symbol, 'expiration_date':expiration_date, 'option_type':option_type, 'strike_price':strike_price})
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
			url 		= '{}/{}'.format(self.BASE_URL, self.OPTIONS_SYMBOL_ENDPOINT),
			params 		= {'underlying':symbol},
			headers 	= self.REQUESTS_HEADERS
		);

		option_list = r.json()['symbols'][0]['options'];

		if df:
			option_df = symbol_list_to_df(option_list);
			option_df['expiration_date'] = parse_option_expiries(option_df['expiration_date']);
			return option_df;

		return option_list;