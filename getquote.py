from config import *



# response = requests.get('https://api.tradier.com/v1/markets/quotes',
#     params={'symbols': 'AAPL,VXX190517P00016000', 'greeks': 'false'},
#     headers={'Authorization': 'Bearer <TOKEN>', 'Accept': 'application/json'}
# )

r = requests.get(
	url 	= '{}/{}'.format(SANDBOX_URL, QUOTES_ENDPOINT),
	params  = {'symbols':'H', 'greeks':'false'},
	headers = {'Authorization':'Bearer {}'.format(AUTH_TOKEN), 'Accept':'application/json'} 
);

r_json = r.json();

print(r_json);