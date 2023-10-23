from config import *

def get_positions(symbols=False, equities=False, options=False):
	'''
	Fetch and filter position data from the Tradier Account API.

	This function makes a GET request to the Tradier Account API to retrieve position
	information related to a trading account. The API response is expected to be in
	JSON format, containing details about the positions held in the account.

	Args:
	    symbols (list, optional): A list of trading symbols (e.g., stock ticker symbols)
	                              to filter the position data. If provided, only positions
	                              matching these symbols will be included.
	    equities (bool, optional): If True, filter the positions to include only equities
	                              (stocks) with symbols less than 5 characters in length.
	                              If False, no filtering based on equities will be applied.
	    options (bool, optional): If True, filter the positions to include only options
	                              with symbols exceeding 5 characters in length.
	                              If False, no filtering based on options will be applied.

	Returns:
	    pandas.DataFrame: A DataFrame containing filtered position information based on
	                      the specified criteria.

	Note:
	    • Before using this function, make sure to define the necessary constants,
	      such as SANDBOX_URL, POSITIONS_ENDPOINT, and REQUESTS_HEADERS, with the
	      appropriate values in a configuration module.

	Example:
	    # Retrieve all positions without filtering
	    all_positions = get_positions()

	    # Retrieve positions for specific symbols ('AAPL', 'GOOGL')
	    specific_positions = get_positions(symbols=['AAPL', 'GOOGL'])

	    # Retrieve only equities
	    equities_positions = get_positions(equities=True)

	    # Retrieve only options
	    options_positions = get_positions(options=True)
	'''
	r = requests.get(url='{}/{}'.format(SANDBOX_URL, ACCOUNT_POSITIONS_ENDPOINT), params={}, headers=REQUESTS_HEADERS);

	positions_df = pd.DataFrame(r.json()['positions']['position']);

	if symbols:
	    positions_df = positions_df.query('symbol in @symbols');

	if equities:
	    positions_df = positions_df[positions_df['symbol'].str.len() < 5];
	    options = False;

	if options:
	    positions_df = positions_df[positions_df['symbol'].str.len() > 5];

	return positions_df;
