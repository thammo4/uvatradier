# Version 3.6.1    
import requests

response = requests.post(
    # url = 'https://api.tradier.com/v1/accounts/{account_id}/orders',
    url = '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
    data={
        'class'             : 'combo',
        'symbol'            : 'SPY',
        'type'              : 'market',
        'duration'          : 'day',
        'price'             : '1.00',

        'side[0]'           : 'buy',
        'quantity[0]'       : '1',
        
        'option_symbol[1]'  : 'SPY140118C00195000',
        'side[1]'           : 'buy_to_open',
        'quantity[1]'       : '100',

        'option_symbol[2]'  : 'SPY140118C00196000',
        'side[2]'           : 'buy_to_close',
        'quantity[2]'       : '100',
        'tag'               : 'my-tag-example-1'
    },
    headers={'Authorization': 'Bearer <TOKEN>', 'Accept': 'application/json'}
)
json_response = response.json()
print(response.status_code)
print(json_response)