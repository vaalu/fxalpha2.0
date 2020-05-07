import json
import csv
import requests
import configparser
import logging
from alice_blue import *
from modules.AliceUtil import AliceUtil
from modules.props.ConfigProps import aliceAnt, AppLogger
from modules.AliceWebSocket import AliceWebSocket

logger = AppLogger()
logger.debug('Fetching access token from alice blue ant API')
config = configparser.ConfigParser()
config.read('application.config.properties')

class Alice():
	access_token = AliceUtil().fetchTokenIfNotExists()
	try:
		alice = AliceBlue(	username=aliceAnt['CLIENT_USER'], 
							password=aliceAnt['CLIENT_PASSWORD'], 
							access_token=access_token, 
							master_contracts_to_download=['NSE', 'MCX'])
	except:
		logger.debug('Unable to fetch token. Abandoning further requests.')
		
	def __init__(self):
		logger.debug('Alice API access:')
		logger.debug('Alice token %s'%(self.access_token))
	
	@classmethod
	def fetchNifty50(self):
		nifty50_list = list([])
		with requests.Session() as csv_session:
			nifty50_csv = csv_session.get(aliceAnt['NIFTY50_URL'])
			decoded_content = nifty50_csv.content.decode('utf-8')
			cr = csv.reader(decoded_content.splitlines(), delimiter=',')
			next(cr)
			nifty50_list = list(cr)
			nifty50_instruments = []
			consolidated_nifty_50_securities = []
			for equity in nifty50_list:
				instr = self.alice.get_instrument_by_symbol(exchange='NSE', symbol=equity[2])
				consolidated_nifty_50_securities.append(instr)
				nifty50_instruments.append([1, instr.token])
			return nifty50_instruments, consolidated_nifty_50_securities
		
	@classmethod
	def fetchCommoditiesV1(self, instruments=[]):
		commodities_instr = list([])
		instr = self.alice.get_instrument_by_symbol(exchange='MCX', symbol='NATURALGAS MAY FUT')
		commodities_instr.append([4, instr.token])
		return commodities_instr
	
	@classmethod
	def fetchNifty50LiveV1(self):
		logger.debug('Establishing websocket connection for instruments ')
		nifty50_instruments, consolidated_nifty_50_securities = self.fetchNifty50()
		logger.debug('Connecting for instruments')
		logger.debug(nifty50_instruments)
		socket_opened = False
		def on_message(msg):
			logger.debug(f'Message recieved: {msg}')
		def on_open():
			global socket_opened
			socket_opened = True
		self.alice.start_websocket(subscribe_callback=on_message,
                      socket_open_callback=on_open,
                      run_in_background=False)
		while(socket_opened==False):
			print('Socket is not opened')
			pass
		self.alice.subscribe(consolidated_nifty_50_securities, LiveFeedType.MARKET_DATA)
		logger.debug('All subscriptions...')
		logger.debug(self.alice.get_all_subscriptions())
		sleep(10)

	@classmethod
	def fetchNifty50Live(self):
		logger.debug('Establishing websocket connection for instruments ')
		nifty50_instruments, consolidated_nifty_50_securities = self.fetchNifty50()
		socket_opened = False
		wssUrl = '%s?access_token='%(aliceAnt['URL_WSS'])
		ws = AliceWebSocket(websocketUrl=wssUrl, token=self.access_token, instruments=nifty50_instruments)
		ws.initialize(ws.instruments)
		print('Websocket is closed...')
	
	@classmethod
	def fetchCommoditiesLive(self):
		commodities = self.fetchCommoditiesV1()
		logger.debug('Establishing websocket connection for instruments ')
		logger.debug(commodities)
		wssUrl = '%s?access_token='%(aliceAnt['URL_WSS'])
		ws = AliceWebSocket(websocketUrl=wssUrl, token=self.access_token, instruments=commodities)
		ws.initialize(ws.instruments)
		print('Websocket is closed...')
	
	@classmethod
	def fetchCommoditiesLiveV1(self):
		commodities = self.fetchCommoditiesV1()
		logger.debug('Establishing websocket connection for instruments ')
		logger.debug(commodities)
		socket_opened = False
		def event_handler_quote_update(message):
			logger.debug(f"quote update {message}")
		def open_callback():
			global socket_opened
			socket_opened = True
		self.alice.start_websocket(subscribe_callback=event_handler_quote_update,
							socket_open_callback=open_callback,
							run_in_background=False)
		while(socket_opened==False):
			pass
		self.alice.subscribe(218567, LiveFeedType.MARKET_DATA)
		sleep(10)

if __name__ == "__main__":
	alice = Alice().fetchCommoditiesLive()