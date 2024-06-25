class Tradier:
	def __init__ (self, account_number, auth_token, live_trade=False):

		#
		# Define account credentials
		#

		self.ACCOUNT_NUMBER 	= account_number;
		self.AUTH_TOKEN 		= auth_token;
		self.REQUESTS_HEADERS 	= {'Authorization':'Bearer {}'.format(self.AUTH_TOKEN), 'Accept':'application/json'}

		
		#
		# Define base url for live/paper trading and individual API endpoints
		#

		self.LIVETRADE_URL 		= 'https://api.tradier.com';
		self.SANDBOX_URL 		= 'https://sandbox.tradier.com';
		self.MARKET_STREAM_URL 	= 'wss://ws.tradier.com';

		self.BASE_URL 		= self.LIVETRADE_URL if live_trade else self.SANDBOX_URL;