from config import *
from datetime import datetime, timedelta;


#
# NOTE - there aren't a lot of option expiry dates, i.e. it isn't just every day
#


#
# APPLY COVERED CALL STRATEGY
#
#   1. Buy 100 shares of Abercrombie & Fitch
#   2. Sell call option on shares with strike price in excess of underlying
#


#
# Place market order for underlying
# (Roughly $50.86 on Aug 23)
#

r = requests.post(
    url     = 'https://sandbox.tradier.com/v1/accounts/{}/orders'.format(ACCOUNT_NUMBER),
    data    = {'class':'equity', 'symbol':'ANF', 'quantity':100, 'side':'buy', 'type':'market', 'duration':'day'},
    headers = {'Authorization':'Bearer {}'.format(AUTH_TOKEN), 'Accept':'application/json'}
);


#
# Place market order to sell call option at higher strike price
#