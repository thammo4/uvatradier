from config import *

def get_gainloss (symbols='', results_limit='', sort_dates='closeDate', sort_symbols='', start_date='', end_date=''):
	params_dict = {'sortBy':sort_dates};

	if results_limit:
		params_dict['limit'] = results_limit;

	if sort_symbols:
		params_dict['sort'] = sort_symbols;

	if start_date:
		params_dict['start'] = start_date;

	if end_date:
		params_dict['end'] = end_date;

	r = requests.get(
		url = '{}/{}'.format(SANDBOX_URL, ACCOUNT_GAINLOSS_ENDPOINT),
		params = params_dict,
		headers = REQUESTS_HEADERS
	);

	gainloss_df = pd.json_normalize(r.json()['gainloss']['closed_position']);

	return gainloss_df;