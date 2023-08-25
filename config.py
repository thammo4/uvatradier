import os;
import dotenv;
import requests;
import pandas as pd;

from datetime import datetime, timedelta; # for fetching option expiries

dotenv.load_dotenv();


#
# Fetch account credentials
#

ACCOUNT_NUMBER 	= os.getenv('tradier_acct');
AUTH_TOKEN 		= os.getenv('tradier_token');


#
# Define headers for convenience because of repeated use with requests
#

REQUESTS_HEADERS = {
	'Authorization' : 'Bearer {}'.format(AUTH_TOKEN),
	'Accept' 		: 'application/json'
}


#
# Define base url for paper trading and individual API endpoints
#

SANDBOX_URL 		= 'https://sandbox.tradier.com';

#
# Account endpoints
#

PROFILE_ENDPOINT 	= "v1/user/profile"; 									# GET
POSITIONS_ENDPOINT 	= "v1/accounts/{}/positions".format(ACCOUNT_NUMBER); 	# GET


#
# Order endpoint
#

ORDER_ENDPOINT = "v1/accounts/{}/orders".format(ACCOUNT_NUMBER); 		# POST



#
# Equity data endpoints
#

QUOTES_ENDPOINT 	= "v1/markets/quotes"; 								# GET (POST)
HISTORICAL_ENDPOINT = "v1/markets/history"; 							# GET



#
# Option data endpoints
#

OPTION_STRIKE_ENDPOINT 	= "v1/markets/options/strikes"; 				# GET
OPTION_CHAIN_ENDPOINT 	= "v1/markets/options/chains"; 					# GET
OPTION_EXPIRY_ENDPOINT 	= "v1/markets/options/expirations"; 			# GET
OPTION_SYMBOL_ENDPOINT 	= "v1/markets/options/lookup"; 					# GET




