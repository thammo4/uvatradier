from .base import Tradier
import requests;
import time;
import asyncio;
import websockets;
import json;

class Stream (Tradier):
	"""
	The Stream class provides a method to connect and stream market data in real time using Tradier's API.
	This class extends the Tradier base class and utilizes both HTTP and WebSocket protocols to establish
	a connection, send subscription requests, and produce incoming market events.

	Note - Per Tradier's documentation, WebSocket streaming is only available via live trading.
		   Ergo, when instantiating the class object, you need to supply the third argument live_trade with its value set to True.

	Attributes:
	- MARKET_STREAM_ENDPOINT (str): API endpoint for market event streaming.
	- ACCOUNT_STREAM_ENDPOINT (str): API endpoint for account event streaming.
	- MARKET_EVENTS_STREAM_ENDPOINT (str): API endpoint for specific market events.

	Methods:
	- stream_market_events: Initiates market event streaming for specified symbols.
	- http_market_stream_connect: Establishes an HTTP connection to get a streaming session ID.
	- ws_market_connect: Connects to a WebSocket to receive and handle live market data.
	"""
	def __init__ (self, account_number, auth_token, live_trade=False):
		"""
		Initialize a new instance of the Stream class which is used for handling real-time
		market data streaming through Tradier's API.

		Parameters:
		- account_number (str): The account number associated with the Tradier account.
		- auth_token (str): The authorization token for API access.
		- live_trade (bool): Flag to indicate if the stream is for live trading or simulation.
		"""
		Tradier.__init__(self, account_number, auth_token, live_trade);

		#
		# Define Streaming Endpoints
		#

		self.MARKET_STREAM_ENDPOINT = "v1/markets/events/session";
		self.ACCOUNT_STREAM_ENDPOINT = "v1/accounts/events/session";
		self.MARKET_EVENTS_STREAM_ENDPOINT = "v1/markets/events";


	#
	# Initiate Market Event Stream
	#

	def stream_market_events (self, symbol_list, filter_list=None, line_break=False, valid_ticks_only=True, advanced_details=True):
		"""
		Start asynchronous market event streaming for a list of symbols.
		This function wraps the asynchronous connection in a synchronous callable method by using asyncio.run.
		Uses asyncio.run to start the websocket connection handling asynchronously.

		Parameters:
		- symbol_list (list): List of market symbols (e.g., ['AAPL', 'GOOGL']) to subscribe to.
		- filter_list (list, optional): List of event types to filter - (Valid Options: 'trade','quote','summary','timesale','tradex')
		- line_break (bool, optional): Whether to include line breaks in the streaming data.
		- valid_ticks_only (bool, optional): Whether to receive only valid ticks.
		- advanced_details (bool, optional): Whether to receive advanced detail level in data.

		Examples:
			stream = Stream(tradier_acct, tradier_token, live_trade=True)
			# Stream all events for ConocoPhillips, Advanced Micro Devices, and Boeing
			stream.stream_market_events(symbol_list=['COP', 'AMD', 'BA'])
			# Stream Kinder Morgan Inc. quotes and trade events with line break separating each event
			stream.stream_market_events(symbol_list=['KMI'], filter_list=['trade', 'quote'], line_break=True)
		"""
		asyncio.run(self.ws_market_connect(symbol_list, filter_list, line_break, valid_ticks_only, advanced_details));


	#
	# Establish HTTP Connection to Tradier
	#

	def http_market_stream_connect (self):
		"""
		Continuously attempt to establish an HTTP connection to the Tradier market stream endpoint
		until a session ID is obtained. Handles reconnection attempts and errors.

		Returns:
		- str: A session ID string used for initiating a WebSocket connection.

		Raises:
		- RuntimeError: If it fails to obtain the session ID after multiple attempts.
		"""
		while True:
			try:
				r = requests.post(url=f"{self.BASE_URL}/{self.MARKET_STREAM_ENDPOINT}", headers=self.REQUESTS_HEADERS);
				r.raise_for_status();

				session_info = r.json();

				# print("API RESPONSE: ", session_info);

				if 'stream' not in session_info:
					print("Error - session_info lacks 'stream'.");
					time.sleep(10);
					continue;

				if 'sessionid' not in session_info['stream']:
					print("Error - 'stream' not in session_info.stream.");
					time.sleep(10);
					continue;

				return session_info['stream']['sessionid'];

			except requests.RequestException as e:
				print(f"API Error: {e}.");
				time.sleep(10);


	#
	# Connect to WebSocket Stream
	#

	async def ws_market_connect (self, symbol_list, filter_list, line_break, valid_ticks_only, advanced_details):
		"""
		Asynchronously connect to the WebSocket stream endpoint and handle market data events.
		This function should not need to be called directly. Use stream_market_events instead.

		Parameters:
		- symbol_list (list): Symbols for which market data is requested.
		- filter_list (list): Specific data event types to filter.
		- line_break (bool): Whether to append line breaks in the received data.
		- valid_ticks_only (bool): Filter to only valid tick events.
		- advanced_details (bool): Request for advanced details in the market data.

		Once connected, sends the specified parameters as a payload and listens for incoming messages.
		"""
		session_id = self.http_market_stream_connect();
		try:
			print(f"Connecting to websocket at {self.WEBSOCKET_URL}/{self.MARKET_EVENTS_STREAM_ENDPOINT} with sessionid {session_id}");
			async with websockets.connect(uri=f"{self.WEBSOCKET_URL}/{self.MARKET_EVENTS_STREAM_ENDPOINT}", ssl=True, compression=None) as websocket:
				payload_json = {
					'symbols': symbol_list,
					'sessionid': session_id,
					'linebreak': line_break,
					'advancedDetails': advanced_details
				};
				if filter_list is not None and isinstance(filter_list, list):
					payload_json['filter'] = filter_list;

				payload = json.dumps(payload_json);

				print(f"Sending: {payload}\n");

				await websocket.send(payload);
				async for message in websocket:
					print(message);

		except websockets.ConnectionClosedError as e:
			print(f"Websocket connection closed but idk why: {e}.");
		except websockets.WebSocketException as e:
			print(f"WebSocket error: {e}.");
		except Exception as e:
			print(f"Unexpected error: {e}.");