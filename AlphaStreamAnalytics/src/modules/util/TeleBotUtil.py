import telegram
from modules.props.ConfigProps import AppProps, AppStrategyLogger
logger = AppStrategyLogger('TeleBotUtil')
class TeleBotUtil():
	__tele_token = AppProps['TELEBOT_TOKEN']
	__tele_chat = AppProps['TELEBOT_CHAT_ID']
	__telebot = None
	__instance = None
	@staticmethod
	def get_instance():
		if TeleBotUtil.__instance == None:
			TeleBotUtil()
		return TeleBotUtil.__instance
	def __init__(self):
		if TeleBotUtil.__instance != None:
			raise Exception('TeleBotUtil is now singleton')
		else:
			TeleBotUtil.__instance = self
			self.__telebot = telegram.Bot(token=self.__tele_token)
			logger.info(self.__telebot.get_me())
	def send_message_01(self, message):
		self.__telebot.send_message(chat_id=self.__tele_chat, text=message, disable_notification = True)
TeleBotUtil()