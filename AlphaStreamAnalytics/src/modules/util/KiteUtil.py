import json
from modules.props.ConfigProps import AppProps, AppKiteLogger
from kiteconnect import KiteConnect
logger = AppKiteLogger.get_instance()
import requests

class KiteUtil():
	__api_key = AppProps["KITE_API_KEY"]
	__api_secret = AppProps["KITE_API_SECRET"]
	__kite = KiteConnect(api_key=__api_key)
	__instance = None
	@staticmethod
	def get_instance():
		if KiteUtil.__instance == None:
			KiteUtil()
		return KiteUtil.__instance
	def __init__(self):
		logger.info('Initializing  kite util')
		if KiteUtil.__instance != None:
			raise Exception('KiteUtil is now singleton')
		else:
			KiteUtil.__instance = self
	def connect(self, req_token):
		logger.info('Connecting to kafka util with token: %s'%req_token)
		logger.info('Kite login url: %s'%self.__kite.login_url())
		resp = self.__kite.generate_session(req_token, self.__api_secret)
		self.__kite.set_access_token(resp["access_token"])
		instruments = self.__kite.instruments(exchange="MCX")
		logger.info('Instrument list from Zerodha: %s'%instruments)

KiteUtil()
	