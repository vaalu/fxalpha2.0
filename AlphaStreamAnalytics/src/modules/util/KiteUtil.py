from modules.props.ConfigProps import AppProps, AppKiteLogger
from kiteconnect import KiteConnect
logger = AppKiteLogger.get_instance()

class KiteUtil():
	__kite = KiteConnect(api_key=AppProps["KITE_API_KEY"])
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
	def connect(self):
		logger.info('Connecting to kafka util')


KiteUtil()
	