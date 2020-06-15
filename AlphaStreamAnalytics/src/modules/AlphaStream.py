import sched
import time
from modules.util.DateTimeUtil import DateTimeUtil
from modules.util.RedisUtil import RedisUtil
from modules.props.ConfigProps import AppOHLCLogger
from modules.OHLCProcessor import OHLCProcessor

logger = AppOHLCLogger('AlphaStream')

class AlphaStream():
	__red_util = RedisUtil.get_instance()
	__all_instruments = list([])
	__equities = list([])
	__commodities = list([])
	__all_instrument_ids = list([])
	__equity_ids = list([])
	__commodity_ids = list([])
	__date_util = DateTimeUtil.get_instance()
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
		today_date = self.__date_util.get_local_date()
		start_time, equities_end_time, commodities_end_time = self.__date_util.get_market_timings()
		
		def get_local_date():
			return today_date
		
		def get_equities_end_time():
			return equities_end_time
		
		def remove_processed_from_cache(sch):
			OHLCProcessor().remove_processed()
		
		# OHLC calc for 5 mins 
		def ohlc_process_05(sch):
			end_time = self.__date_util.get_local_time()
			minutes_05 = 60 * 5
			start_time = end_time - minutes_05
			str_start = self.__date_util.get_from_timestamp(start_time)
			str_end = self.__date_util.get_from_timestamp(end_time)
			instruments = self.__all_instrument_ids if start_time < get_equities_end_time() else self.__commodity_ids
			OHLCProcessor().process_all_from_cache_with_limit(instruments,start_time,end_time,5)
			delta = minutes_05 - (self.__date_util.get_current_local_time() % minutes_05)
			logger.info('Processing between %f - %f - %s : %s - Next on: %f seconds'%(start_time, end_time, str_start, str_end, delta))
			ohlc_scheduler.enter(5,1,remove_processed_from_cache,(sch,))
		
		def ohlc_process_01(sch):
			end_time = self.__date_util.get_local_time()
			minutes_01 = 60
			start_time = end_time - minutes_01
			str_start = self.__date_util.get_from_timestamp(start_time)
			str_end = self.__date_util.get_from_timestamp(end_time) 
			instruments = self.__all_instrument_ids if start_time < get_equities_end_time() else self.__commodity_ids
			delta = minutes_01 - (self.__date_util.get_current_local_time() % minutes_01) 
			logger.info('Processing between %f - %f - %s : %s - Next : %f seconds'%(start_time, end_time, str_start, str_end, delta))
			ohlc_scheduler.enter(delta,1,ohlc_process_01,(sch,))
			OHLCProcessor().process_all_from_cache_with_limit(instruments,start_time,end_time,1)
			if end_time % 300 == 0:
				ohlc_scheduler.enter(5,1,ohlc_process_05,(sch,))
		
		def eod_calc():
			process_start_01 = self.__date_util.get_custom_time(9, 0, 0) 
			logger.info('Process starts by %i'%process_start_01)
			day_end = self.__date_util.get_custom_time(23, 30, 0) 
			time_limit = 60
			OHLCProcessor().process_all_from_cache_with_limit(self.__all_instrument_ids,process_start_01,process_start_01+time_limit,1)
			while process_start_01 < day_end:
				logger.info('Processing ...%s'%(self.__date_util.get_from_timestamp(process_start_01)))
				OHLCProcessor().process_all_from_cache_with_limit(self.__all_instrument_ids,process_start_01,process_start_01+time_limit,1)
				process_start_01 = process_start_01 + time_limit
		
		def eod_calc_5():
			process_start_01 = self.__date_util.get_custom_time(9, 0, 0) 
			logger.info('Process starts by %i'%process_start_01)
			day_end = self.__date_util.get_custom_time(23, 30, 0) 
			time_limit = 60  * 5
			while process_start_01 < day_end:
				logger.info('Processing ...%s'%(self.__date_util.get_from_timestamp(process_start_01))) 
				OHLCProcessor().process_all_from_cache_with_limit(self.__all_instrument_ids,process_start_01,process_start_01+time_limit,5)
				process_start_01 = process_start_01 + time_limit
		
		def eod_save(sch):
			logger.info('EOD process: saving daily data - 1 min')
			EODProcessor().initialize_1_min_process(self.__all_instrument_ids)

		ohlc_scheduler = sched.scheduler(time.time, time.sleep)
		logger.info('Current date: %s'%get_local_date())
		current_minute = time.mktime(get_local_date().timetuple())
		delta = 60 - (time.mktime(get_local_date().timetuple()) % 60)
		logger.info('Time delta: %f'%delta) 

		logger.info('Current millisecond Next : %f'%(delta))
		# eod_calc()
		# eod_calc_5()
		# remove_processed_from_cache(ohlc_scheduler)
		ohlc_scheduler.enter(delta,1,ohlc_process_01,(ohlc_scheduler,))
		ohlc_scheduler.run()
	