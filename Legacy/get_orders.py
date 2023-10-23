from config import *

#
# Fetch current order queue
#

def get_orders ():
	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		params 	= {'includeTags':'true'},
		headers = REQUESTS_HEADERS
	);

	return pd.DataFrame(r.json()['orders']['order']);