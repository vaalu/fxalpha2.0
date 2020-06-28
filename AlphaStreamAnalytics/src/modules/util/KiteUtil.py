from modules.props.ConfigProps import AppProps, AppKiteLogger
from kiteconnect import KiteConnect
logger = AppKiteLogger.get_instance()

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
	def connect(self):
		logger.info('Connecting to kafka util')
		logger.info('Kite login url: %s'%self.__kite.login_url())
		data = self.__kite.generate_session("2Bx0dKFB7CMuBpU2CV9vfbiIt8ObpEvC", api_secret=self.__api_secret)
		self.__kite.set_access_token(data["access_token"])
		self.__kite.instruments()


KiteUtil()
	