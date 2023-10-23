from config import *

#
# Implement straddle option strategy (long/short)
#

def straddle_order (symbol, option0, quantity0, option1, quantity1, side, duration='day'):
	'''
		Place a long-straddle or short-straddle order on the given underlying symbol.

		Args:
			symbol: underlying asset of option contracts
			option0: call leg of the straddle
			quantity0: number of call contracts
			option1: put leg of the straddle
			quantity1: number of put contracts
			side: ['long', 'short']
			duration: day, gtc, pre, post

		Returns:
			json response to confirm success.

		Example:
			# determine the current price of a given underlying
			last_price = get_quote_day('UDR', last_price=True)

			option0 = option_chain_day('UDR', strike_low=40, strike_high=40, option_type='call')['symbol']
			option1 = option_chain_day('UDR', strike_low=40, strike_high=40, option_type='put')['symbol']

			straddle_order(symbol='UDR', option0=option0, quantity0=1.0, option1=option1, quantity1=1.0, side='long', duration='gtc')
				{'order': {'id': 7780584, 'status': 'ok', 'partner_id': '3a8bbee1-5184-4ffe-8a0c-294fbad1aee9'}}
	'''

	#
	# Check that trade_side is either long (long straddle) or short (short straddle)
	#

	trade_side = '';

	if side.lower() not in ['long', 'short']:
		return 'Need the side to be either "long" or "short"';

	if side.lower() == 'long':
		trade_side = 'buy_to_open';
	if side.lower() == 'short':
		trade_side = 'sell_to_open';

	r = requests.post(
		url 	= '{}/{}'.format(SANDBOX_URL, ORDER_ENDPOINT),
		data 	= {
			'class' 			: 'multileg',
			'symbol' 			: symbol,
			'type' 				: 'market',
			'duration' 			: duration,
			'option_symbol[0]' 	: option0,
			'side[0]' 			: trade_side,
			'quantity[0]' 		: quantity0,
			'option_symbol[1]' 	: option1,
			'side[1]' 			: trade_side,
			'quantity[1]' 		: quantity1
		},
		headers = REQUESTS_HEADERS
	);

	return r.json();