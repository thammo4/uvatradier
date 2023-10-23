from config import *

from get_orders import get_orders;

def rejected_order_by_symbol (symbol_rejected):
	df_orders = get_orders();
	return int(df_orders.query('symbol==@symbol_rejected & status=="rejected"')['id']);