from config import *
from main import *
import time



# equity_market_order(symbol, side, quantity, duration='day')
#     This function will place a simple market order for the supplied symbol.
#     By default, the order is good for the day. Per the nature of market orders, it should be filled.
    
#     Parameter Notes:
#             side            = buy, buy_to_cover, sell, sell_short
#             duration        = day, gtc, pre, post

# def print_hello_world_every_5_minutes():
def test_buy_sell ():
    while True:
        # print("Hello, World")
        print('Buying KLAC'); equity_market_order(symbol='KLAC', side='buy', quantity=10.0, duration='day'); time.sleep(15);
        print('Selling KLAC'); equity_market_order(symbol='KLAC', side='sell', quantity=10.0, duration='day'); time.sleep(15);

test_buy_sell();
