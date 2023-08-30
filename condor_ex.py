from main import *

put1 = list(option_chain_day ('FTV').query('strike == 70.0 & option_type == "put"')['symbol'])[0];
put2 = list(option_chain_day ('FTV').query('strike == 75.0 & option_type == "put"')['symbol'])[0];

call1 = list(option_chain_day('FTV').query('strike == 80.0 & option_type == "call"')['symbol'])[0];
call2 = list(option_chain_day('FTV').query('strike == 85.0 & option_type == "call"')['symbol'])[0];



#
# Submit order for put credit spread
#

# side[index]	Form	String	Required	buy_to_open	
# The side of the leg. One of: buy_to_open, buy_to_close, sell_to_open, sell_to_close

response = requests.post(
	url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
    data 	= {
    	'class': 'multileg',
    	'symbol': 'FTV',
    	'type': 'market',
    	'duration': 'gtc',

    	'option_symbol[0]': put1,
    	'side[0]': 'buy_to_open',
    	'quantity[0]': '2',

    	'option_symbol[1]': put2,
    	'side[1]': 'sell_to_open',
    	'quantity[1]': '2'
    },
    headers = REQUESTS_HEADERS
);


#
# Submit order for call credit spread
#

response = requests.post(
	url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
    data 	= {
    	'class': 'multileg',
    	'symbol': 'FTV',
    	'type': 'market',
    	'duration': 'gtc',

    	'option_symbol[0]': call1,
    	'side[0]': 'sell_to_open',
    	'quantity[0]': '2',

    	'option_symbol[1]': call2,
    	'side[1]': 'buy_to_open',
    	'quantity[1]': '2'
    },
    headers = REQUESTS_HEADERS
)





print('put1 = {}'.format(put1))
print('put2 = {}'.format(put2))
print('call1 = {}'.format(call1))
print('call2 = {}'.format(call2))