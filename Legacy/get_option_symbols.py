from config import *


#
# This function returns a list of symbols. Each element has a format
# 	COP240216C00115000
#
# i.e.
#
# 	COP 240216 C 00115000
#

def get_option_symbols (underlying_symbol, df=False):
	'''
		This function provides a convenient wrapper to fetch option symbols
		for a specified underlying_symbol
	'''
	r = requests.get(
		url 		= '{}/{}'.format(SANDBOX_URL, OPTION_SYMBOL_ENDPOINT),
		params 		= {'underlying':underlying_symbol},
		headers 	= REQUESTS_HEADERS
	);

	option_list = r.json()['symbols'][0]['options'];

	if df:
		option_df = symbol_list_to_df(option_list);
		option_df['expiration_date'] = parse_option_expiries(option_df['expiration_date']);
		return option_df;

	return option_list;




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