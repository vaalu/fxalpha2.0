from modules.props.ConfigProps import AppOHLCLogger
from modules.util.RedisUtil import RedisUtil
from modules.util.DateTimeUtil import DateTimeUtil

logger = AppOHLCLogger('OHLCProcessor')
date_util = DateTimeUtil()
def process_ohlc(red_util, topic, start_time, end_time, duration, duration_key):
	while start_time < end_time:
		# logger.info('Processing... %s:%s'%(topic, date_util.get_iso_from_timestamp(start_time)))
		red_util.fetch_between(topic, start_time, start_time+duration, duration_key)
		start_time = start_time + duration

def process_ohlc_5(red_util, topic, start_time, end_time, duration, duration_key):
	while start_time < end_time:
		logger.info('Processing... %s:%s'%(topic, date_util.get_iso_from_timestamp(start_time)))
		red_util.fetch_between_5(topic, start_time, start_time+duration, duration_key)
		start_time = start_time + duration

class OHLCProcessor():
	
	__red_util = RedisUtil()
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
	def remove_processed(self):
		self.__red_util.remove_processed()
