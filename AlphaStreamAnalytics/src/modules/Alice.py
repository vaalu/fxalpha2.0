import json
import csv
import requests
import logging
from alice_blue import *
from modules.AliceUtil import AliceUtil
from modules.util.RedisUtil import RedisUtil
from modules.props.ConfigProps import AppProps, AppLogger
from modules.AliceWebSocket import AliceWebSocket
from modules.util.SingleInstanceUtil import SingleInstanceUtil

logger = AppLogger('Alice')
logger.debug('Fetching access token from alice blue ant API')

class Alice():
	access_token = AliceUtil.get_instance().fetchTokenIfNotExists()
	__single_instance_util = SingleInstanceUtil()
	__instruments_util = __single_instance_util.get_instrument_util()
	__red_util = RedisUtil.get_instance()
	try:
		alice = AliceBlue(	username=AppProps['CLIENT_USER'], 
							password=AppProps['CLIENT_PASSWORD'], 
							access_token=access_token, 
							master_contracts_to_download=['NSE', 'MCX'])
	except:
		logger.debug('Unable to fetch token. Abandoning further requests.')
		
	def __init__(self):
		logger.debug('Alice API access:')
		logger.debug('Alice token %s'%(self.access_token))

	@classmethod
	def fetchNifty50(self):
		nifty50_instruments, consolidated_nifty_50_securities = self.__instruments_util.fetchNifty50()
		return nifty50_instruments, consolidated_nifty_50_securities
	
	@classmethod
	def fetchCommodities(self):
		commodities_instr, commodities_token_list = self.__instruments_util.fetch_commodities()
		return commodities_instr, commodities_token_list
	
	@classmethod
	def fetchCommoditiesV1(self, instruments=[]):
		commodities_instr, commodities_token_list = self.fetchCommodities()
		return commodities_token_list
	
	@classmethod
	def fetchNifty50Live(self):
		logger.debug('Establishing websocket connection for instruments ')
		nifty50_instruments, consolidated_nifty_50_securities = self.fetchNifty50()
		socket_opened = False
		wssUrl = '%s?access_token='%(AppProps['URL_WSS'])
		ws = AliceWebSocket(websocketUrl=wssUrl, token=self.access_token, instruments=nifty50_instruments)
		ws.initialize(ws.instruments)
		print('Websocket is closed...')
	
	@classmethod
	def fetchCommoditiesLive(self):
		commodities = self.fetchCommoditiesV1()
		logger.debug('Establishing websocket connection for instruments ')
		logger.debug(commodities)
		wssUrl = '%s?access_token='%(AppProps['URL_WSS'])
		ws = AliceWebSocket(websocketUrl=wssUrl, token=self.access_token, instruments=commodities)
		ws.initialize(ws.instruments)
		print('Websocket is closed...')

	@classmethod
	def initiaize_instruments(self):
		nifty50_instruments, consolidated_nifty_50_securities = self.fetchNifty50()
		commodities_instr, commodities_token_list = self.fetchCommodities()
		all_instruments = list([])
		all_instruments.extend(consolidated_nifty_50_securities)
		all_instruments.extend(commodities_instr)
		self.__red_util.add_processing_instruments(all_instruments)

if __name__ == "__main__":
	alice = Alice().initiaize_instruments()