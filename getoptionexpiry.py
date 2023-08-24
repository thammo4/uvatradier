from config import *



#
# Wrapper function to get contract expiration dates
#

def get_expiry_dates (symbol, strikes=False):
	'''
		This returns a list of valid dates on which option contracts expire.
	'''
	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, OPTION_EXPIRY_ENDPOINT),
		params 	= {'symbol':symbol, 'includeAllRoots':True, 'strikes':str(strikes)},
		headers = REQUESTS_HEADERS
	);

	if r.status_code != 200:
		return 'wtf';

	expiry_dict = r.json()['expirations'];

	# Without strikes, we can get a list of dates
	if strikes == False:
		return expiry_dict['date'];

	# Otherwise, return a list whose elements are dicts with format {'date':[list_of_strikes]}
	return expiry_dict['expiration'];