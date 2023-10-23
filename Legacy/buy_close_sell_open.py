from main import *

#
# Simple script to buy Microsoft at the end of the trading day and sell it at the start of the trading day.
#

def buy_MSFT ():
	print ('Buying MSFT');
	equity_market_order (symbol='MSFT', side='buy', quantity=10.0, duration='day');
	print('Done.\n');

def sell_MSFT ():
	print ('Selling MSFT');
	equity_market_order (symbol='MSFT', side='sell', quantity=10.0, duration='day');
	print ('Done.\n');


schedule.every().day.at("15:59:00").do(buy_MSFT);
schedule.every().day.at("09:33:00").do(sell_MSFT);

print('Running Buy/Sell MSFT script...\n');
while True:
	schedule.run_pending();
	time.sleep(1);
