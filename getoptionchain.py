from config import *
from datetime import datetime, timedelta;


#
# NOTE - there aren't a lot of option expiry dates, i.e. it isn't just every day
#




#
# Fetch option chain data 

# date_to_use = '2023-10-20';
# date_to_use = '2023-09-08';
date_to_use = '2025-12-19';
r = requests.get(
    url     = 'https://sandbox.tradier.com/v1/markets/options/chains',
    params  = {'symbol': 'HAL', 'expiration':date_to_use, 'greeks':'true'},
    headers = {'Authorization':'Bearer {}'.format(AUTH_TOKEN), 'Accept':'application/json'}
);

option_chain = r.json()['options']['option'];


print(r.json());





# json_response = response.json()
# print(response.status_code)
# print(json_response)


# r = requests.get(
#     url     = 'https://sandbox.tradier.com/v1/markets/options/chains',
#     params  = {'symbol':'DD', 'expiration':'2023-08-25', 'greeks':'true'},
#     headers = {'Authorization':'Bearer {}'.format(AUTH_TOKEN), 'Accept':'application/json'}
# );

# print(r.json());


#
# Fetch option strike prices for DuPont
#


