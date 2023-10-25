class Tradier:
	def __init__ (self, account_number, auth_token):

		#
		# Define account credentials
		#

		self.ACCOUNT_NUMBER 	= account_number;
		self.AUTH_TOKEN 		= auth_token;
		self.REQUESTS_HEADERS 	= {'Authorization':'Bearer {}'.format(self.AUTH_TOKEN), 'Accept':'application/json'}

		
		#
		# Define base url for paper trading and individual API endpoints
		#

		self.SANDBOX_URL = 'https://sandbox.tradier.com';