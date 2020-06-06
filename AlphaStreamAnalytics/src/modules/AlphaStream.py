import sched
import time
import pytz
from datetime import datetime
from dateutil import tz
from modules.util.RedisUtil import RedisUtil
from modules.util.SingleInstanceUtil import SingleInstanceUtil
from modules.props.ConfigProps import AppLogger
from modules.OHLCProcessor import OHLCProcessor

logger = AppLogger('AlphaStream')

class AlphaStrem():
	__single_instance_util = SingleInstanceUtil()
	__instruments_util = __single_instance_util.get_instrument_util()
	__red_util = RedisUtil()
	__all_instruments = list([])
	__equities = list([])
	__commodities = list([])
	__all_instrument_ids = list([])
	__equity_ids = list([])
	__commodity_ids = list([])
	__offset = offset = datetime.now(pytz.timezone('Asia/Kolkata')).utcoffset().total_seconds()
	def __init__(self):
		logger.info('Initializing stream processing')
		self.__equities = self.__red_util.fetch_processing_instruments('EQUITY')
		self.__commodities = self.__red_util.fetch_processing_instruments('COMMODITY')
		self.__all_instruments.extend(self.__equities)
		self.__all_instruments.extend(self.__commodities)
		for instrument in self.__equities: self.__equity_ids.append(instrument["token"])
		for instrument in self.__commodities: self.__commodity_ids.append(instrument["token"])
		for instrument in self.__all_instruments: self.__all_instrument_ids.append(instrument["token"])
		logger.info(self.__equity_ids)
		logger.info(self.__commodity_ids)
		logger.info(self.__all_instrument_ids)
	def process_ohlc(self):
		def get_local_date():
			return datetime.now().astimezone(tz.gettz('Asia/Kolkata'))
		def get_local_time():
			return time.mktime(get_local_date().replace(second=0, microsecond=0).timetuple()) # - self.__offset
		def get_equities_end_time():
			return time.mktime(get_local_date().replace(hour=15, second=30, microsecond=0).timetuple())
		def remove_processed_from_cache(sch):
			OHLCProcessor().remove_processed()
		# OHLC calc for 5 mins 
		def ohlc_process_05(sch):
			end_time = get_local_time()
			minutes_05 = 60 * 5
			start_time = end_time - minutes_05
			str_start = datetime.fromtimestamp(start_time).isoformat()
			str_end = datetime.fromtimestamp(end_time).isoformat()
			instruments = self.__all_instrument_ids if start_time < get_equities_end_time() else self.__commodity_ids
			OHLCProcessor().process_all_from_cache_with_limit(instruments,start_time,end_time,5)
			delta = minutes_05 - (time.mktime(datetime.now().timetuple()) % minutes_05)
			logger.info('Processing between %f - %f - %s : %s - Next on: %f seconds'%(start_time, end_time, str_start, str_end, delta))
			ohlc_scheduler.enter(5,1,remove_processed_from_cache,(sch,))
		def ohlc_process_01(sch):
			end_time = get_local_time()
			minutes_01 = 60
			start_time = end_time - minutes_01
			str_start = datetime.fromtimestamp(start_time).isoformat()
			str_end = datetime.fromtimestamp(end_time).isoformat()
			instruments = self.__all_instrument_ids if start_time < get_equities_end_time() else self.__commodity_ids
			OHLCProcessor().process_all_from_cache_with_limit(instruments,start_time,end_time,1)
			if end_time % 300 == 0:
				ohlc_scheduler.enter(5,1,ohlc_process_05,(sch,))
			if (end_time + 60) <= time.mktime(datetime.now().timetuple()):
				ohlc_scheduler.enter(0,1,ohlc_process_01,(sch,))
			delta = minutes_01 - (time.mktime(datetime.now().timetuple()) % minutes_01)
			logger.info('Processing between %f - %f - %s : %s - Next : %f seconds'%(start_time, end_time, str_start, str_end, delta))
			ohlc_scheduler.enter(delta,1,ohlc_process_01,(sch,))

		ohlc_scheduler = sched.scheduler(time.time, time.sleep)
		logger.info('Current date: %s'%get_local_date())
		current_minute = time.mktime(get_local_date().timetuple())
		delta = 60 - (time.mktime(get_local_date().timetuple()) % 60)
		logger.info('Time delta: %f'%delta) 

		logger.info('Current millisecond Next : %f'%(delta))
		ohlc_scheduler.enter(delta,1,ohlc_process_01,(ohlc_scheduler,))
		ohlc_scheduler.run()
	