#
# This script demonstrates how to:
# 	• Read account number and authorization token from .env file in working directory
# 	• Instantiate uvatradier class objects for Account, Quotes, and OptionsData
#

import os, dotenv;
from uvatradier import Tradier, Account, Quotes, OptionsData;

#
# Check that .env file exists
#

dotenv.load_dotenv();
if not dotenv.load_dotenv():
	quit();


#
# Fetch account number and auth token
#

tradier_acct = os.getenv('tradier_acct');
tradier_token = os.getenv('tradier_token');


#
# Instantiate uvatradier class objects
#

account = Account(tradier_acct, tradier_token);
quotes 	= Quotes(tradier_acct, tradier_token);
options = OptionsData(tradier_acct, tradier_token);



