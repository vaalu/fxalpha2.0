import time
import sched
import datetime
import json
from modules.AlphaConsumerLegacy import AlphaConsumerLegacy
from modules.props.ConfigProps import AppLogger, AppProperties
from modules.OHLCProcessor import OHLCProcessor
from modules.EODProcessing import EODProcessor

logger = AppLogger()

ohlc_scheduler = sched.scheduler(time.time, time.sleep)
ohlc_scheduler_5min = sched.scheduler(time.time, time.sleep)

topics = ['218567']
commodities = ['218567']
# mapped_instruments = alpha.fetch_all_instruments_with_info()

logger.info('All the instruments: %s'%str(topics))
logger.info('Commodities: %s'%str(commodities))

today_date = datetime.datetime.now()
time_tuple = datetime.datetime(today_date.year, today_date.month, today_date.day, 9, 0, 0).timetuple()
start_time=int(time.mktime(time_tuple))
end_time_equities=time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day, 15, 30, 0).timetuple())

process_start_01 = start_time
process_start_05 = start_time
process_start_15 = start_time
process_start_30 = start_time
process_start_60 = start_time

def remove_processed_from_cache(sch):
	OHLCProcessor().remove_processed()

# OHLC calc for 5 mins 
def ohlc_process_05(sch):
	duration = 60 * 5
	now_date = datetime.datetime.now()
	process_init = time.mktime(now_date.replace(second=0).timetuple())
	process_start_05 = time.mktime(now_date.replace(second=0).timetuple()) - duration
	logger.info('Processing 5min %f'%process_start_05)
	time_limit = duration
	print(time_limit)
	instruments = topics if process_init < end_time_equities else commodities
	OHLCProcessor().process_all_from_cache_with_limit(instruments,process_start_05,process_start_05+time_limit,5)
	process_start_05 = process_start_05 + time_limit
	logger.info('Waiting for next 5M ...%s'%(datetime.datetime.fromtimestamp(process_start_05).isoformat() ))
	curr_time = time.mktime(datetime.datetime.now().timetuple())
	if curr_time > process_start_05:
		OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_05-5,process_start_05+(curr_time-process_start_05),1)
		process_start_05=process_start_05 + curr_time
	ohlc_scheduler.enter(10,1,remove_processed_from_cache,(sch,))

# OHLC calc for 1 min 
def ohlc_process_01(sch):
	now_date = datetime.datetime.now()
	process_init = time.mktime(now_date.replace(second=0).timetuple()) + 60
	process_start_01 = time.mktime(now_date.replace(second=0).timetuple()) - 60
	process_init_time = time.mktime(now_date.replace(second=0).timetuple())
	time_limit = 60 * 1
	instruments = topics if process_init < end_time_equities else commodities
	OHLCProcessor().process_all_from_cache_with_limit(instruments,process_start_01,process_start_01+time_limit,1)
	process_start_01 = process_start_01 + time_limit
	logger.info('Waiting for next 1M ...%s'%(datetime.datetime.fromtimestamp(process_start_01).isoformat() ))
	curr_time = time.mktime(datetime.datetime.now().replace(second=0).timetuple())
	if curr_time > process_start_01:
		OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_01-5,process_start_01+(curr_time-process_start_01),1)
		process_start_01=process_start_01 + curr_time
		process_init = time.mktime(now_date.replace(second=0).timetuple()) + 60
	time_delta = (process_init - time.mktime(datetime.datetime.now().timetuple()))
	logger.info('Next calculation starts in %f seconds'%time_delta)
	if process_init_time % (60*5) == 0:
		logger.info('Initializing 5Min calculation')
		ohlc_scheduler_5min.enter(0,1,ohlc_process_05,(ohlc_scheduler,))
		ohlc_scheduler_5min.run()
	ohlc_scheduler.enter(time_delta,1,ohlc_process_01,(sch,))

def eod_calc():
	process_start_01 = time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day-2, 9, 0, 0).timetuple())
	day_end = time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day-2, 22, 30, 0).timetuple())
	OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_01,process_start_01+60,1)
	while process_start_01 < day_end:
		time_limit = 60
		logger.info('Processing ...%s'%(datetime.datetime.fromtimestamp(process_start_01).isoformat() ))
		OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_01,process_start_01+time_limit,1)
		process_start_01 = process_start_01 + time_limit

def eod_calc_5():
	process_start_01 = time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day-2, 9, 0, 0).timetuple())
	day_end = time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day-2,23, 30, 0).timetuple())
	while process_start_01 < day_end:
		time_limit = 60  * 5
		logger.info('Processing ...%s'%(datetime.datetime.fromtimestamp(process_start_01).isoformat() ))
		OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_01,process_start_01+time_limit,5)
		process_start_01 = process_start_01 + time_limit

def eod_save(sch):
	logger.info('EOD process: saving daily data - 1 min')
	EODProcessor().initialize_1_min_process(topics)

# Initializing one min ohlc
zeroth_sec = time.mktime(datetime.datetime.now().replace(second=0).timetuple()) + 15
print('To be initiated 1M at %s'%(datetime.datetime.fromtimestamp(zeroth_sec).isoformat()))
curr_time = time.mktime(datetime.datetime.now().timetuple())

ohlc_scheduler.enter(zeroth_sec-curr_time,1,ohlc_process_01,(ohlc_scheduler,))

# eod_save(ohlc_scheduler)
eod_calc()
eod_calc_5()
remove_processed_from_cache(ohlc_scheduler)
# ohlc_scheduler.run()
