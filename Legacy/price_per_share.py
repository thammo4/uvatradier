from config import *
from get_positions import get_positions;

def price_per_share (symbol):
	'''
	Calculate the price-per-share for a equity/option symbol that you currently own.

	This function computes the price-per-share of a symbol found in the `get_positions` returned dataframe.
	It filters the `get_positions` data, calculates the price-per-share, and returns the value as a float.

	Arguments:
		symbol (str): The trading symbol (e.g., stock symbol or OCC option symbol) whose price-per-share is desired.

	Returns:
		float: The computed price-per-share.
	'''
	record = get_positions().query('symbol == @symbol');
	return float(record['cost_basis'] / record['quantity']);
