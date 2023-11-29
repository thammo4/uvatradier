#
# Example - Using lumiwealth_tradier to fetch quote data for a given symbol
#

import os

import dotenv

from lumiwealth_tradier import Quotes

# Create .env file within current working directory.
# Add the following to your .env file. Specify the correct account number and authorization token for your quote.
# tradier_acct = <ACCOUNT_NUMBER>
# tradier_token = <AUTH_TOKEN>

dotenv.load_dotenv()

tradier_acct = os.getenv('tradier_acct')
tradier_token = os.getenv('tradier_token')

# Initializing new Quotes object
quotes = Quotes(tradier_acct, tradier_token)

test_quote = quotes.get_quote_day('KO')

print(test_quote)
