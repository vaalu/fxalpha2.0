import datetime
import time
from modules.util.RedisUtil import RedisUtil

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

		print('Start time of the day...%i'%(self.__timewise_calc["start_time"]))
		print('End of the day for equities...%i'%(self.__timewise_calc["end_time_equities"]))
		print('End of the day for commodities...%i'%(self.__timewise_calc["end_time_commodities"]))
		self.prepare_duration_list()
	
	def prepare_list(self, duration_in_mins, duration_key):
		print('Duration of candlestick data: %i'%(duration_in_mins))
		end_duration_in_seconds=duration_in_mins*60 if duration_in_mins > 0 else 1
		cache_keys = list([])
		index = self.__timewise_calc["start_time"]
		end_time = self.__timewise_calc["end_time_commodities"]
		while index < end_time:
			index = index + end_duration_in_seconds
			cache_keys.append(index)
		self.__timewise_calc[duration_key] = cache_keys

	def prepare_duration_list(self):
		print('Preparing duration of 1 second')
		self.prepare_list(0, "seconds_list")
		print('Preparing duration of 1 min')
		self.prepare_list(1, "01_minute_list")
		print('Preparing duration of 5 min')
		self.prepare_list(5, "05_minute_list")
		print('Preparing duration of 15 min')
		self.prepare_list(15, "15_minute_list")
		print('Preparing duration of 30 min')
		self.prepare_list(30, "30_minute_list")
		print('Preparing duration of 60 min')
		self.prepare_list(60, "60_minute_list")
	
	def read_from_cache(self, topics_to_process, start_time):
		print('Preparing for processing: ')
		print('Minute-wise data')
		self.__red_util.fetch_between(218567, start_time, start_time+60)
	
	def process_all_from_cache(self, topics_to_process, time_limit):
		# 1589203834
		index = self.__timewise_calc["start_time"]
		if topics_to_process != None:
			while index < time_limit:
				for topic in topics_to_process:
					print('Processing topic ', topic)
					self.__red_util.fetch_all(str(topic), str(index))
				index = index + 1
	def process_for_ohlc(self):
		self.read_from_cache(start_time, duration)