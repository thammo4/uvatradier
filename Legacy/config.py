import os;
import dotenv;
import requests;
import numpy as np;
import pandas as pd;

import datetime;
from datetime import datetime, timedelta; 	# for fetching option expiries
import re; 									# parsing option symbols into constituent components

import schedule;
import time;

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

PROFILE_ENDPOINT 			= "v1/user/profile"; 									# GET

POSITIONS_ENDPOINT 			= "v1/accounts/{}/positions".format(ACCOUNT_NUMBER); 	# GET


ACCOUNT_BALANCE_ENDPOINT 	= "v1/accounts/{}/balances".format(ACCOUNT_NUMBER); 	# GET
ACCOUNT_GAINLOSS_ENDPOINT 	= "v1/accounts/{}/gainloss".format(ACCOUNT_NUMBER);
ACCOUNT_HISTORY_ENDPOINT 	= "v1/accounts/{}/history".format(ACCOUNT_NUMBER); 		# GET
ACCOUNT_POSITIONS_ENDPOINT 	= "v1/accounts/{}/positions".format(ACCOUNT_NUMBER); 	# GET


#
# Order endpoint
#

ORDER_ENDPOINT = "v1/accounts/{}/orders".format(ACCOUNT_NUMBER); 					# POST



#
# Equity data endpoints
#

QUOTES_ENDPOINT 			= "v1/markets/quotes"; 											# GET (POST)
QUOTES_HISTORICAL_ENDPOINT 	= "v1/markets/history"; 										# GET
QUOTES_TIMESALES_ENDPOINT 	= "v1/markets/timesales"; 										# GET
QUOTES_SEARCH_ENDPOINT 		= "v1/markets/search"; 											# GET



#
# Option data endpoints
#

OPTION_STRIKE_ENDPOINT 	= "v1/markets/options/strikes"; 							# GET
OPTION_CHAIN_ENDPOINT 	= "v1/markets/options/chains"; 								# GET
OPTION_EXPIRY_ENDPOINT 	= "v1/markets/options/expirations"; 						# GET
OPTION_SYMBOL_ENDPOINT 	= "v1/markets/options/lookup"; 								# GET



#
# Intraday market status endpoint
#

CLOCK_ENDPOINT = "v1/markets/clock"; 												# GET



#
# Market calendar endpoint
#

CALENDAR_ENDPOINT = 'v1/markets/calendar'; 											# GET
