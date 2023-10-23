# event.py

class Event(object):
    """
    Event is base class providing an interface for all subsequent 
    (inherited) events, that will trigger further events in the 
    trading infrastructure.   
    """
    pass


# event.py

class MarketEvent(Event):
    """
    Handles the event of receiving a new market update with 
    corresponding bars.
    """

    def __init__(self):
        """
        Initialises the MarketEvent.
        """
        self.type = 'MARKET'




class SignalEvent (Event):
    def __init__ (self, symbol, datetime, signal_type):
        '''
        Initialize SignalEvent object.

        Params:
            symbol = stock (e.g. 'AAPL')
            datetime = timestamp of when event occurred
            signal_type = 'LONG' or 'SHORT'
        '''

        self.type = 'SIGNAL';
        self.symbol = symbol;
        self.datetime = datetime;
        self.signal_type = signal_type;





class OrderEvent (Event):
    '''
    Sends orders to execution system.
    '''

    def __init__ (self, symbol, order_type, quantity, direction):
        '''
        Params:
            symbol = asset
            order_type = 'MRK', 'LMT'
            quantity = non-negative integer
            direction = 'BUY', 'SELL'
        '''

        self.type = 'ORDER';
        self.symbol = symbol;
        self.order_type = order_type;
        self.quantity = quantity;
        self.direction = direction;

    def print_order (self):
        print("Order: Symbol={symbol}, Type={type}, Quantity={quantity}, Direction={direction}".format(symbol=self.symbol, type=self.type, quantity=self.quantity, direction=self.direction)); 




class FillEvent (Event):
    def __init__ (self, timeindex, symbol, exchange, quantity, direction, fill_cost, commission=None):
        self.type = 'FILL';
        self.timeindex = timeindex;
        self.symbol = symbol;
        self.exchange = exchange;
        self.quantity = quantity;
        self.direction = direction;
        self.fill_cost = fill_cost;
        self.commission = commission;





# event.py

# class FillEvent(Event):
#     """
#     Encapsulates the notion of a Filled Order, as returned
#     from a brokerage. Stores the quantity of an instrument
#     actually filled and at what price. In addition, stores
#     the commission of the trade from the brokerage.
#     """

#     def __init__(self, timeindex, symbol, exchange, quantity, 
#                  direction, fill_cost, commission=None):
#         """
#         Initialises the FillEvent object. Sets the symbol, exchange,
#         quantity, direction, cost of fill and an optional 
#         commission.

#         If commission is not provided, the Fill object will
#         calculate it based on the trade size and Interactive
#         Brokers fees.

#         Parameters:
#         timeindex - The bar-resolution when the order was filled.
#         symbol - The instrument which was filled.
#         exchange - The exchange where the order was filled.
#         quantity - The filled quantity.
#         direction - The direction of fill ('BUY' or 'SELL')
#         fill_cost - The holdings value in dollars.
#         commission - An optional commission sent from IB.
#         """
        
#         # self.type = 'FILL'
#         # self.timeindex = timeindex
#         # self.symbol = symbol
#         # self.exchange = exchange
#         # self.quantity = quantity
#         # self.direction = direction
#         # self.fill_cost = fill_cost

#         # # Calculate commission
#         # if commission is None:
#         #     self.commission = self.calculate_ib_commission()
#         # else:
#         #     self.commission = commission







