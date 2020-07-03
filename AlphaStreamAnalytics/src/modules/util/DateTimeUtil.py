import pytz
import time
from datetime import datetime, timedelta
from dateutil import tz
from modules.props.ConfigProps import AppLogger, AppProps

logger = AppLogger('DateTimeUtil')

class DateTimeUtil():
	__time_zone = AppProps['TIME_ZONE']
	__offset = datetime.now(pytz.timezone('Asia/Kolkata')).utcoffset().total_seconds() if __time_zone == 'utc' else 0
	__today_date = datetime.now().astimezone(tz.gettz('Asia/Kolkata')) # - timedelta(days=1)
	__prev_date = datetime.now().astimezone(tz.gettz('Asia/Kolkata')) - timedelta(days=1)
	__offset_delta = {
		"hour": __offset//3600 if __time_zone == 'utc' else 0, 
		"min": (__offset//60)%60 if __time_zone == 'utc' else 0, 
	}
	__instance = None
	
	@staticmethod
	def get_instance():
		if DateTimeUtil.__instance == None:
			DateTimeUtil()
		return DateTimeUtil.__instance
	def __init__(self):
		if DateTimeUtil.__instance != None:
			raise Exception('DateTime util is now singleton')
		else:
			DateTimeUtil.__instance = self
	def get_local_date(self):
		local_dt = datetime.now().astimezone(tz.gettz('Asia/Kolkata')) #  - timedelta(days=1)
		return local_dt 
	def get_local_prev_date(self):
		local_dt = datetime.now().astimezone(tz.gettz('Asia/Kolkata')) - timedelta(days=1)
		return local_dt 
	def get_current_local_time(self):
		return time.mktime(self.get_local_date().replace(second=0,microsecond=0).timetuple()) - self.__offset
	def get_local_time(self):
		return time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, 9, 30, 0).timetuple()) - self.__offset
	def get_ist_offset(self):
		return self.__offset
	def get_from_timestamp(self, time_val):
		return datetime.fromtimestamp(time_val) # .isoformat()
	def get_start_time(self):
		return time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, 9, 30, 0).timetuple()) - self.__offset
	def get_end_time_equities(self):
		return time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, 15, 30, 0).timetuple()) - self.__offset
	def get_end_time_commodities(self):
		return time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, 23, 30, 0).timetuple()) - self.__offset
	def get_market_timings(self):
		start_time = self.get_start_time()
		end_time_equities = self.get_end_time_equities()
		end_time_commodities = self.get_end_time_commodities()
		logger.info('Start: %i : equities end: %i : commodities end: %i'%(start_time, end_time_equities, end_time_commodities))
		return start_time, end_time_equities, end_time_commodities
	def get_start_time_prev(self):
		return time.mktime(datetime(self.__prev_date.year, self.__prev_date.month, self.__prev_date.day, 9, 30, 0).timetuple()) - self.__offset
	def get_end_time_equities_prev(self):
		return time.mktime(datetime(self.__prev_date.year, self.__prev_date.month, self.__prev_date.day, 15, 30, 0).timetuple()) - self.__offset
	def get_end_time_commodities_prev(self):
		return time.mktime(datetime(self.__prev_date.year, self.__prev_date.month, self.__prev_date.day, 23, 30, 0).timetuple()) - self.__offset
	def get_market_timings_previous_day(self):
		start_time = self.get_start_time_prev()
		end_time_equities = self.get_end_time_equities_prev()
		end_time_commodities = self.get_end_time_commodities_prev()
		return start_time, end_time_equities, end_time_commodities
	def get_strategy_closure_timings(self):
		end_time_equities = time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, 14, 45, 0).timetuple()) - self.__offset
		end_time_commodities = time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, 23, 0, 0).timetuple()) - self.__offset
		return end_time_equities, end_time_commodities
	def get_strategy_closure_positions(self):
		psn_cls_equities = time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, 15, 15, 0).timetuple()) - self.__offset
		psn_cls_commodities = time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, 23, 15, 0).timetuple()) - self.__offset
		return psn_cls_equities, psn_cls_commodities
	def get_custom_time(self, hh, mnt, scnd):
		return time.mktime(datetime(self.__today_date.year, self.__today_date.month, self.__today_date.day, hh, mnt, scnd).timetuple())
DateTimeUtil()