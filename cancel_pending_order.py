from config import *

#
# HTTP delete call to order endpoint
#

def cancel_pending_order (order_id):
	'''
		This function will set the order status to 'canceled' for an order whose status was 'pending'.
		To get the order_id argument, use the get_orders function.
	'''

	ORDER_CANCEL_ENDPOINT = "v1/accounts/{}/orders/{}".format(ACCOUNT_NUMBER, order_id);

	r = requests.delete(
		url 	= "{}/{}".format(SANDBOX_URL, ORDER_CANCEL_ENDPOINT),
		data 	= {},
		headers = REQUESTS_HEADERS
	);

	return r.json();