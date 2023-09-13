from tradier import *



dotenv.load_dotenv();


#
# Fetch account credentials from .env file
#

ACCOUNT_NUMBER 	= os.getenv('tradier_acct');
AUTH_TOKEN 		= os.getenv('tradier_token');


account = Account(ACCOUNT_NUMBER, AUTH_TOKEN);
quotes 	= Quotes(ACCOUNT_NUMBER, AUTH_TOKEN);
options = OptionsData(ACCOUNT_NUMBER, AUTH_TOKEN);


options_order = OptionsOrder(ACCOUNT_NUMBER, AUTH_TOKEN);




#
# Bear Call Spread
#

# for example, if hban = $10.70, then let S(t) = 10.70 ; K1 = 12.50 ; K2 = 15.0

hban = quotes.get_quote_day('HBAN', last_price=True);

# Define the short call and long call legs of the spread
leg0 = options.get_chain_day('HBAN', strike=12.50, option_type='call')['symbol'];
leg1 = options.get_chain_day('HBAN', strike=15.00, option_type='call')['symbol'];

# Successful options order will return JSON with the following format
# {'order': {'id': 8028987, 'status': 'ok', 'partner_id': '3a8bbee1-5184-4ffe-8a0c-294fbad1aee9'}}
options_order.bear_call_spread(underlying='HBAN', option0=leg0, quantity0=1.0, option1=leg1, quantity1=1.0, duration='gtc');