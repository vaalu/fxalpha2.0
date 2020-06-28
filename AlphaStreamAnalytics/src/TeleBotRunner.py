from modules.util.TeleBotUtil import TeleBotUtil
if __name__ == "__main__":
	telebot = TeleBotUtil.get_instance()
	telebot.send_message_01('Test message')