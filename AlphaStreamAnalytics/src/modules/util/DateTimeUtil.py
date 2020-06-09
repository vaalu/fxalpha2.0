import pytz
import time
from datetime import datetime
from dateutil import tz
from modules.props.ConfigProps import AppLogger, AppProps

logger = AppLogger('CalculationsProcessor')

class DateTimeUtil():
	__offset = datetime.now(pytz.timezone('Asia/Kolkata')).utcoffset().total_seconds()
	__today_date = datetime.now().astimezone(tz.gettz('Asia/Kolkata'))
	def get_local_date(self):
		return datetime.now().astimezone(tz.gettz('Asia/Kolkata'))
	def get_local_time(self):
		return time.mktime(self.get_local_date().replace(second=0, microsecond=0).timetuple()) # - self.__offset
	def get_start_time(self):
		return time.mktime(self.get_local_date().replace(hour=9, second=0, microsecond=0).timetuple())
	def get_end_time_equities(self):
		return time.mktime(self.get_local_date().replace(hour=15, second=30, microsecond=0).timetuple())
	def get_end_time_commodities(self):
		return time.mktime(self.get_local_date().replace(hour=23, second=30, microsecond=0).timetuple())
	def get_market_timings(self):
		start_time = self.get_start_time()
		end_time_equities = self.get_end_time_equities()
		end_time_commodities = self.get_end_time_commodities()
		return start_time, end_time_equities, end_time_commodities