from config import *

def get_positions(symbols=False):
	'''
	Fetch and return position data from the Tradier Account API.

	This function makes a GET request to the Tradier Account API to retrieve position
	information related to a trading account. The API response is expected to be in
	JSON format, containing details about the positions held in the account.

	Returns:
		pandas.DataFrame: A DataFrame containing position information.

	Note:
		• Before using this function, make sure to define the necessary constants,
		  such as SANDBOX_URL, POSITIONS_ENDPOINT, and REQUESTS_HEADERS, with the
		  appropriate values in a configuration module.
		• You can optionally provide a list of trading symbols (symbols) to filter the
		  position data for specific symbols.

	Example:
		position_data = get_positions()
		print(position_data)

		# To filter position data for specific symbols:
		symbols_to_filter = ['AAPL', 'GOOGL']
		filtered_data = get_positions(symbols_to_filter)
		print(filtered_data)
	'''
	r = requests.get(url='{}/{}'.format(SANDBOX_URL, POSITIONS_ENDPOINT), params={}, headers=REQUESTS_HEADERS)

	positions_df = pd.DataFrame(r.json()['positions']['position'])

	if symbols:
		positions_df = positions_df.query('symbol in @symbols')

	return positions_df
