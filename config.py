import os;
import dotenv;
import requests;
import pandas as pd;

dotenv.load_dotenv();

ACCOUNT_NUMBER 	= os.getenv('tradier_acct');
AUTH_TOKEN 		= os.getenv('tradier_token');


#
# Define base url for paper trading and individual API endpoints
#

SANDBOX_URL 		= 'https://sandbox.tradier.com';
PROFILE_ENDPOINT 	= "v1/user/profile"; 								# GET
ORDER_ENDPOINT 		= "v1/accounts/{}/orders".format(ACCOUNT_NUMBER); 	# POST
QUOTES_ENDPOINT 	= "v1/markets/quotes";

OPTION_STRIKE_ENDPOINT = "v1/markets/options/strikes";