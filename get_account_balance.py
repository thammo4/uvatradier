from config import *

def get_account_balance ():
	r = requests.get(
		url 	= '{}/{}'.format(SANDBOX_URL, ACCOUNT_BALANCE_ENDPOINT),
		params 	= {},
		headers = REQUESTS_HEADERS
	);

	return pd.json_normalize(r.json()['balances']);