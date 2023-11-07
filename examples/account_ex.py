#
# Example - Using uvatradier to fetch account balance information
#

import os, dotenv;
from uvatradier import Tradier, Account;

# Create .env file within current working directory.
# Add the following to your .env file. Specify the correct account number and authorization token for your account.
# 	tradier_acct = <ACCOUNT_NUMBER>
#	tradier_token = <AUTH_TOKEN>

dotenv.load_dotenv();

tradier_acct = os.getenv('tradier_acct');
tradier_token = os.getenv('tradier_token');

# Initialize a new Account object
account = Account(tradier_acct, tradier_token);

# Fetch account balance info
balance = account.get_account_balance();

print(balance);
