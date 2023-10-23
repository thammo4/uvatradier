import datetime;
import os, os.path;
from abc import ABCMeta, abstractmethod;
from event import MarketEvent;



class DataHandler (object):
	'''
	Abstract Base Class

	Derived DataHandler classes should output OHLCV vars for each requested symbol.
	Replicates live strategy that encounters market data sequentially
	'''

	__metaclass__ = ABCMeta;

	@abstractmethod
	def get_latest_bars (self, symbol, N=1):
		raise NotImplementedError('Implement get_latest_bars()');

	@abstractmethod
	def update_bars (self):
		raise NotImplementedError('Implement update_bars()');


class HistoricCSVDataHandler (DataHandler):
	def __init__ (self, events, csv_dir, symbol_list):
		self.events = events;
		self.csv_dir = csv_dir;
		self.symbol_list = symbol_list;

		self.symbol_data = {};
		self.latest_symbol_data = {};
		self.continue_backtest = True;

		self._open_convert_csv_files();