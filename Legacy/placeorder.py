from config import *

#
# Place market order to buy 10 shares of Microsoft
#

r = requests.post(
    url     = '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
    headers = {'Authorization': 'Bearer {}'.format(AUTH_TOKEN), 'Accept':'application/json'},
    data    = {'class':'equity','symbol': 'MSFT','side':'buy','quantity': '10','type': 'market','duration': 'day','tag': 'my-tag-example-1'}
);

r_response = r.json();
print(r_response);