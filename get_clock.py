from config import *


def get_clock ():
	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, CLOCK_ENDPOINT),
		params 	= {'delayed':'false'},
		headers = REQUESTS_HEADERS
	);

	return pd.json_normalize(r.json()['clock']);

