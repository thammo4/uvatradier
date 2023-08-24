from config import *

def get_positions ():
	r = requests.get(url='{}/{}'.format(SANDBOX_URL, POSITIONS_ENDPOINT), params={}, headers=REQUESTS_HEADERS);

	return pd.DataFrame(r.json()['positions']['position']);
