import pytz
import time
from datetime import datetime, timedelta
from dateutil import tz
from modules.props.ConfigProps import AppLogger, AppProps

logger = AppLogger('CalculationsProcessor')

class DateTimeUtil():
	__time_zone = AppProps['TIME_ZONE']
	__offset = datetime.now(pytz.timezone('Asia/Kolkata')).utcoffset().total_seconds() if __time_zone == 'utc' else 0
	__today_date = datetime.now().astimezone(tz.gettz('Asia/Kolkata')) # - timedelta(days=1)
	__offset_delta = {
		"hour": __offset//3600 if __time_zone == 'utc' else 0, 
		"min": (__offset//60)%60 if __time_zone == 'utc' else 0, 
	}
	def get_local_date(self):
		return datetime.now() # .astimezone(tz.gettz('Asia/Kolkata'))
	def get_current_local_time(self):
		return time.mktime(datetime.now().timetuple()) - self.__offset
	def get_local_time(self):
		return  time.mktime(get_local_date().replace(second=0, microsecond=0).timetuple()) - self.__offset
	def get_previous_day(self):
		return self.get_local_date() - timedelta(days=1)
	def get_previous_day_start_time(self):
		prev_date = self.get_previous_day()
		return time.mktime(datetime(prev_date.year, prev_date.month, prev_date.day, 9, 0, 0).timetuple()) - self.__offset
	def get_previous_day_equity_end_time(self):
		prev_date = self.get_previous_day()
		return time.mktime(datetime(prev_date.year, prev_date.month, prev_date.day, 15, 30, 0).timetuple()) - self.__offset
	def get_previous_day_commodities_end_time(self):
		today_date = self.get_previous_day()
		return time.mktime(datetime(today_date.year, today_date.month, today_date.day, 23, 30, 0).timetuple()) - self.__offset
	def get_local_time(self):
		return time.mktime(self.get_local_date().replace(second=0, microsecond=0).timetuple()) - self.__offset
	def get_ist_offset(self):
		return self.__offset
	def get_iso_from_timestamp(self, time_val):
		return datetime.fromtimestamp(time_val).isoformat()
	def get_start_time(self):
		return time.mktime(self.get_local_date().replace(hour=9, second=0, microsecond=0).timetuple()) - self.__offset
	def get_end_time_equities(self):
		return time.mktime(self.get_local_date().replace(hour=15, second=30, microsecond=0).timetuple()) - self.__offset
	def get_end_time_commodities(self):
		return time.mktime(self.get_local_date().replace(hour=23, second=30, microsecond=0).timetuple()) - self.__offset
	def get_market_timings(self):
		start_time = self.get_start_time()
		end_time_equities = self.get_end_time_equities()
		end_time_commodities = self.get_end_time_commodities()
		return start_time, end_time_equities, end_time_commodities
	def get_market_timings_previous_day(self):
		start_time = self.get_previous_day_start_time()
		end_time_equities = self.get_previous_day_equity_end_time()
		end_time_commodities = self.get_previous_day_commodities_end_time()
		return start_time, end_time_equities, end_time_commodities
	def get_custom_time(self, hh, mnt, scnd):
		return time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, hh, mnt, scnd).timetuple())
