import time
import pytz
import redis
from modules.props.ConfigProps import AppLogger
from modules.util.RedisUtil import RedisUtil
from datetime import datetime
from dateutil import tz
logger = AppLogger('DataCleanUp')

class DataCleanUp():
	__red = redis.Redis(host='localhost', port=6379, decode_responses=True)
	__red_util = RedisUtil()
	__all_instrument_ids = list([])
	__total_batches_for_cleanup = 0
	def __init__(self):
		logger.info('Data cleanup initialized...')
		__all_instruments = list([])
		__equities = self.__red_util.fetch_processing_instruments('EQUITY')
		__commodities = self.__red_util.fetch_processing_instruments('COMMODITY')
		__all_instruments.extend(__equities)
		__all_instruments.extend(__commodities)
		for instrument in __all_instruments: self.__all_instrument_ids.append(instrument["token"])
		logger.info(self.__all_instrument_ids)
	def __tz_offset(self):
		diff = datetime.now(pytz.timezone('Asia/Kolkata')).utcoffset().total_seconds()
		return diff + 5
		# return 0
	def __now(self):
		return datetime.now().astimezone(tz.gettz('Asia/Kolkata')).replace(second=0)
	def __now_time(self):
		return time.mktime(self.__now().replace(second=0).timetuple()) - self.__tz_offset()
	def __today_timings(self):
		today_date = self.__now()
		curr_start_time = time.mktime(datetime(today_date.year, today_date.month, today_date.day, 9, 0, 0).timetuple())
		curr_end_time = time.mktime(datetime(today_date.year, today_date.month, today_date.day, 23, 30, 0).timetuple())
		return curr_start_time, curr_end_time
	def split_as_batch(self, iterable, batch_size):
		for indx in range(0, len(iterable), batch_size):
			yield iterable[indx:indx + batch_size]
	def find_keys(self):
		trade_start_time, trade_end_time = self.__today_timings()
		logger.info('Trade timings at %i : %i'%(trade_start_time, trade_end_time))
		processing_time = trade_start_time
		batches = []
		# while processing_time < trade_end_time:
		for instrument in self.__all_instrument_ids:
			key_pattern = '%s:315513000*'%(instrument)
			keys = self.__red.keys(key_pattern)
			all_keys = self.split_as_batch(keys, 500)
			total = sum(1 for _ in all_keys)
			self.__total_batches_for_cleanup = self.__total_batches_for_cleanup + total
			logger.info('Checking for pattern %s : %i'%(key_pattern, total))
			batches.extend(self.split_as_batch(keys, 500))
		for batch in batches:
			logger.info('Remaining batches to cleanup: %i'%self.__total_batches_for_cleanup)
			for key in batch:
				self.__red.delete(key)
			self.__total_batches_for_cleanup = self.__total_batches_for_cleanup - 1

if __name__ == "__main__":
	DataCleanUp().find_keys()