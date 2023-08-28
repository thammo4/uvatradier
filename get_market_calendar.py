from config import *


def get_market_calendar (month=False, year=False, days_df=False):
	params = {};

	if month:
		params['month'] = month;
	if year:
		params['year'] = year;

	r = requests.get(
		url = '{}/{}'.format(SANDBOX_URL, CALENDAR_ENDPOINT),
		params = params,
		headers = REQUESTS_HEADERS
	);

	if days_df:
		return pd.DataFrame(r.json()['calendar']['days']['day']);

	return r.json()['calendar'];