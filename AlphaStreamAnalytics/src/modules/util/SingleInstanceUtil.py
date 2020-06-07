from datetime import datetime, tzinfo
import pytz
import time
from dateutil import tz
from modules.props.ConfigProps import AppLogger, AppProps
from modules.util.AliceInstrumentsUtil import AliceInstruments

logger = AppLogger('SingleInstanceUtil')
class SingleInstanceUtil():
	__alice_instruments = AliceInstruments()
	def __init__(self):
		logger.info('Initializing singleton instances for the application')
	def __tz_offset(self):
		# Offset difference
		return datetime.now(pytz.timezone('Asia/Kolkata')).utcoffset().total_seconds() + 5
		# return 0
	def __now(self):
		return datetime.now().astimezone(tz.gettz('Asia/Kolkata')).replace(second=0)
	def __now_time(self):
		return time.mktime(self.__now().replace(second=0).timetuple()) - self.__tz_offset()
	def get_today_local_date(self):
		return datetime.now().astimezone(tz.gettz('Asia/Kolkata'))
	def today_timings(self):
		today_date = self.__now()
		curr_start_time = time.mktime(datetime(today_date.year, today_date.month, today_date.day, 9, 0, 0).timetuple()) -self.__tz_offset()
		curr_end_time = time.mktime(datetime(today_date.year, today_date.month, today_date.day, 23, 30, 0).timetuple()) -self.__tz_offset()
		return curr_start_time, curr_end_time, self.__tz_offset()
	def get_instrument_util(self):
		return self.__alice_instruments
