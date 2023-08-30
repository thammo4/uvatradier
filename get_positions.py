from config import *

def get_positions ():

	'''
	Fetches and returns position data from the Tradier Account API.

    This function makes a GET request to the Tradier Account API to retrieve position
    information related to a trading account. The API response is expected to be in
    JSON format, containing details about the positions held in the account.

    Returns:
        pandas.DataFrame: A DataFrame containing position information.

    Note:
        Before using this function, make sure to define the necessary constants,
        such as SANDBOX_URL, POSITIONS_ENDPOINT, and REQUESTS_HEADERS, with the
        appropriate values in a configuration module.

    Example:
        position_data = get_positions()
        print(position_data)
    '''

	r = requests.get(url='{}/{}'.format(SANDBOX_URL, POSITIONS_ENDPOINT), params={}, headers=REQUESTS_HEADERS);

	return pd.DataFrame(r.json()['positions']['position']);
