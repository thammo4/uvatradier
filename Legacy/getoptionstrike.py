from config import *
from datetime import datetime, timedelta;

next_week = (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d');

url = "{}/{}".format(SANDBOX_URL, OPTION_STRIKE_ENDPOINT);


#
# Fetch strike prices on DuPont options whose expiration occurs in three days
#

r = requests.get(
	url 	= url,
	params 	= {'symbol':'DD', 'expiration':next_week},
	headers = {'Authorization':'Bearer {}'.format(AUTH_TOKEN), 'Accept':'application/json'}
);