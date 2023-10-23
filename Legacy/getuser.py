from config import *

#
# Fetch basic account information
#

def get_profile ():
	'''
		This function returns basic information about user account.
	'''

	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, PROFILE_ENDPOINT),
		params 	= {},
		headers = REQUESTS_HEADERS
	);

	return pd.json_normalize(r.json()['profile']);