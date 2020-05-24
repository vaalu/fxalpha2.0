import datetime
import time
from modules.props.ConfigProps import AppLogger
from modules.util.RedisUtil import RedisUtil

logger = AppLogger()

def process_ohlc(red_util, topic, start_time, end_time, duration, duration_key):
	while start_time < end_time:
		logger.info('Processing... %s:%s'%(topic, datetime.datetime.fromtimestamp(start_time).isoformat()))
		red_util.fetch_between(topic, start_time, start_time+duration, duration_key)
		start_time = start_time + duration

def process_ohlc_5(red_util, topic, start_time, end_time, duration, duration_key):
	while start_time < end_time:
		logger.info('Processing... %s:%s'%(topic, datetime.datetime.fromtimestamp(start_time).isoformat()))
		red_util.fetch_between_5(topic, start_time, start_time+duration, duration_key)
		start_time = start_time + duration

class OHLCProcessor():
	
	__start_time = 0
	__end_of_day_equities = 0
	__end_of_day_commodities = 0
	__red_util = RedisUtil()
	__timewise_calc = {
		"start_time":0,
		"end_time_equities":0,
		"end_time_commodities":0,
		"seconds_list":[],
		"01_minute_list":[],
		"05_minute_list":[],
		"15_minute_list":[],
		"30_minute_list":[],
		"60_minute_list":[]
	}
	
	def __init__(self):
		
		print('Initializing OHLC Processor')
		
		today_date = datetime.datetime.now()
		time_tuple = datetime.datetime(today_date.year, today_date.month, today_date.day, 10, 0, 0).timetuple()
		self.__timewise_calc["start_time"]=int(time.mktime(time_tuple))

		time_tuple = datetime.datetime(today_date.year, today_date.month, today_date.day, 15, 30, 0).timetuple()
		self.__timewise_calc["end_time_equities"]=int(time.mktime(time_tuple))
		
		time_tuple = datetime.datetime(today_date.year, today_date.month, today_date.day, 23, 30, 0).timetuple()
		self.__timewise_calc["end_time_commodities"]=int(time.mktime(time_tuple))

		self.prepare_duration_list()
	
	def prepare_list(self, duration_in_mins, duration_key):
		logger.info('Duration of candlestick data: %i'%(duration_in_mins))
		end_duration_in_seconds=duration_in_mins*60 if duration_in_mins > 0 else 1
		cache_keys = list([])
		index = self.__timewise_calc["start_time"]
		end_time = self.__timewise_calc["end_time_commodities"]
		while index < end_time:
			index = index + end_duration_in_seconds
			cache_keys.append(index)
		self.__timewise_calc[duration_key] = cache_keys

	def prepare_duration_list(self):
		self.prepare_list(0, "seconds_list")
		self.prepare_list(1, "01_minute_list")
		self.prepare_list(5, "05_minute_list")
		self.prepare_list(15, "15_minute_list")
		self.prepare_list(30, "30_minute_list")
		self.prepare_list(60, "60_minute_list")
	
	def process_all_from_cache_with_limit(self, topics_to_process, tstart_time, tend_time, duration):
		index = tstart_time
		if topics_to_process != None and duration == 1:
			limit = 60 * duration # 1 min
			for topic in topics_to_process:
				process_ohlc(self.__red_util, topic, index, tend_time, limit, "%iM"%(duration))
		elif topics_to_process != None and duration == 5:
			limit = 60 * duration # 5 min
			for topic in topics_to_process:
				process_ohlc_5(self.__red_util, topic, index, tend_time, limit, "%iM"%(duration))