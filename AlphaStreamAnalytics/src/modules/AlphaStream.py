import sched
import time
from datetime import datetime
from dateutil import tz
from modules.util.RedisUtil import RedisUtil
from modules.util.SingleInstanceUtil import SingleInstanceUtil
from modules.props.ConfigProps import AppLogger
from modules.OHLCProcessor import OHLCProcessor

logger = AppLogger()

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
	def __init__(self):
		print('Initializing stream processing')
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
	def __now(self):
		return datetime.now().astimezone(tz.gettz('Asia/Kolkata')).replace(second=0)
	def process_ohlc(self):
		print('Process starting for ohlc')
		ohlc_scheduler = sched.scheduler(time.time, time.sleep)
		ohlc_scheduler_5min = sched.scheduler(time.time, time.sleep)
		today_date = self.__now()
		end_time_equities = time.mktime((self.__now().replace(hour=15, minute=30, second=0)).timetuple())
		logger.info('Equities time-off: %s'%str(end_time_equities))
		def remove_processed_from_cache(sch):
			OHLCProcessor().remove_processed()
		# OHLC calc for 5 mins 
		def ohlc_process_05(sch):
			duration = 60 * 5
			now_date = self.__now()
			process_init = time.mktime(now_date.replace(second=0).timetuple())
			process_start_05 = time.mktime(now_date.replace(second=0).timetuple())
			time_limit = duration
			logger.info('Processing 5min %f'%(process_start_05))
			instruments = self.__all_instrument_ids if process_init < end_time_equities else self.__commodity_ids
			OHLCProcessor().process_all_from_cache_with_limit(instruments,process_start_05,process_start_05+time_limit,5)
			process_start_05 = process_start_05 + time_limit
			logger.info('Waiting for next 5M ...%s'%(datetime.fromtimestamp(process_start_05).isoformat() ))
			curr_time = time.mktime(self.__now().timetuple())
			if curr_time > process_start_05:
				OHLCProcessor().process_all_from_cache_with_limit(self.__all_instrument_ids,process_start_05-5,process_start_05+(curr_time-process_start_05),1)
				process_start_05=process_start_05 + curr_time
			ohlc_scheduler.enter(10,1,remove_processed_from_cache,(sch,))
		# OHLC calc for 1 min 
		def ohlc_process_01(sch):
			now_date = self.__now()
			now_date.replace(second=0)
			process_init = time.mktime(now_date.timetuple()) + 60
			process_start_01 = time.mktime(now_date.timetuple()) - 60
			process_init_time = time.mktime(now_date.timetuple())
			time_limit = 60 * 1
			instruments = self.__all_instrument_ids if process_init < end_time_equities else self.__commodity_ids
			OHLCProcessor().process_all_from_cache_with_limit(instruments,process_start_01,process_start_01+time_limit,1)
			process_start_01 = process_start_01 + time_limit
			logger.info('Waiting for next 1M ...%s'%(datetime.fromtimestamp(process_start_01 + time_limit).isoformat() ))
			curr_time = time.mktime(self.__now().replace(second=0).timetuple())
			if curr_time > process_start_01:
				OHLCProcessor().process_all_from_cache_with_limit(self.__all_instrument_ids,process_start_01-5,process_start_01+(curr_time-process_start_01),1)
				process_start_01=process_start_01 + curr_time
				process_init = time.mktime(now_date.timetuple()) + 60
			time_delta = (process_init - time.mktime(self.__now().timetuple()))
			logger.info('Next calculation starts in %f seconds'%time_delta)
			if process_init_time % (60*5) == 0:
				logger.info('Initializing 5Min calculation')
				ohlc_scheduler_5min.enter(0,1,ohlc_process_05,(ohlc_scheduler,))
				ohlc_scheduler_5min.run()
			ohlc_scheduler.enter(time_delta,1,ohlc_process_01,(sch,))
		def eod_calc():
			process_start_01 = time.mktime(datetime(today_date.year, today_date.month, today_date.day, 9, 0, 0).timetuple())
			day_end = time.mktime(datetime(today_date.year, today_date.month, today_date.day, 23, 30, 0).timetuple())
			OHLCProcessor().process_all_from_cache_with_limit(self.__all_instrument_ids,process_start_01,process_start_01+60,1)
			while process_start_01 < day_end:
				time_limit = 60
				logger.info('Processing ...%s'%(datetime.fromtimestamp(process_start_01).isoformat() ))
				OHLCProcessor().process_all_from_cache_with_limit(self.__all_instrument_ids,process_start_01,process_start_01+time_limit,1)
				process_start_01 = process_start_01 + time_limit
		def eod_calc_5():
			process_start_01 = time.mktime(datetime(today_date.year, today_date.month, today_date.day, 9, 0, 0).timetuple())
			day_end = time.mktime(datetime(today_date.year, today_date.month, today_date.day,23, 30, 0).timetuple())
			while process_start_01 < day_end:
				time_limit = 60  * 5
				logger.info('Processing ...%s'%(datetime.fromtimestamp(process_start_01).isoformat() ))
				OHLCProcessor().process_all_from_cache_with_limit(self.__all_instrument_ids,process_start_01,process_start_01+time_limit,5)
				process_start_01 = process_start_01 + time_limit
		def eod_save(sch):
			logger.info('EOD process: saving daily data - 1 min')
			EODProcessor().initialize_1_min_process(self.__all_instrument_ids)
		# Initializing one min ohlc
		zeroth_sec = time.mktime(datetime.now().replace(second=0).timetuple()) + 15
		print('To be initiated 1M at %s'%(datetime.fromtimestamp(zeroth_sec).isoformat()))
		curr_time = time.mktime(datetime.now().timetuple())
		ohlc_scheduler.enter(zeroth_sec-curr_time,1,ohlc_process_01,(ohlc_scheduler,))
		# eod_save(ohlc_scheduler)
		# eod_calc()
		# eod_calc_5()
		# remove_processed_from_cache(ohlc_scheduler)
		ohlc_scheduler.run()