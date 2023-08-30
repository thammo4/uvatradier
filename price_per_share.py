from config import *
from get_positions import get_positions;

def price_per_share (symbol):
	record = get_positions().query('symbol == @symbol');
	return float(record['cost_basis'] / record['quantity']);