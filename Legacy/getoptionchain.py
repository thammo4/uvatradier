from config import *
from getoptionexpiry import get_expiry_dates;



#
# Fetch all option chain data for a single day of contract expirations
#

def option_chain_day (symbol, expiry='', strike_low=False, strike_high=False, option_type=False):
	'''
		This function returns option chain data for a given symbol.
		All contract expirations occur on the same expiry date
	'''

	#
	# Set the contract expiration date to the nearest valid date
	#

	if not expiry:
		expiry = get_expiry_dates(symbol)[0];

	#
	# Define request object for given symbol and expiration
	#

	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, OPTION_CHAIN_ENDPOINT),
		params 	= {'symbol':symbol, 'expiration':expiry, 'greeks':'false'},
		headers = REQUESTS_HEADERS
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

	if option_type in ['call', 'put']:
		option_df = option_df.query('option_type == @option_type');


	if option_type:
		if option_type in ['call', 'put']:
			option_df = option_df.query('option_type == @option_type');

	#
	# Return the resulting dataframe whose rows are individual contracts with expiration `expiry`
	#

	return option_df;

















