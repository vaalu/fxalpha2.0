import time
import sched
import datetime
from modules.props.ConfigProps import AppLogger, AppProperties
from modules.OHLCProcessor import OHLCProcessor
from kafka import KafkaConsumer

logger = AppLogger()

ohlc_scheduler = sched.scheduler(time.time, time.sleep)

class AlphaStream():
	ohlc_processor = OHLCProcessor()
	kafka_server = '%s:%s'%(AppProperties['KAFKA_URL'], AppProperties['KAFKA_PORT'])
	init_consumer = KafkaConsumer(	bootstrap_servers=[kafka_server], 
								api_version=(0, 10), 
								consumer_timeout_ms=1000)
	topics = init_consumer.topics()
	logger.debug('All topics that are present: ')
	logger.debug(topics)
	def __init__(self):
		logger.debug('Initializing AlphaStream')

	def fetch_topics(self):
		return self.topics

	def process_stream(self):
		curr_time = 1589281800
		logger.info('Started processing streams...until %f'%(curr_time) )
		self.ohlc_processor.process_all_from_cache(['218567'], curr_time)
		# self.ohlc_processor.read_from_cache(['218567'], curr_time)

# AlphaStream().process_stream()

topics = AlphaStream().fetch_topics()
today_date = datetime.datetime.now()
time_tuple = datetime.datetime(today_date.year, today_date.month, today_date.day, 9, 0, 0).timetuple()
start_time=int(time.mktime(time_tuple))


process_start_01 = start_time
process_start_05 = start_time
process_start_15 = start_time
process_start_30 = start_time
process_start_60 = start_time

def ohlc_process_01(sch):
	now_date = datetime.datetime.now()
	process_init = time.mktime(now_date.replace(second=0).timetuple()) + 60
	process_start_01 = time.mktime(now_date.replace(second=0).timetuple()) - 60
	time_limit = 60 * 1
	OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_01,process_start_01+time_limit,1)
	process_start_01 = process_start_01 + time_limit
	logger.info('Waiting for next ...%s'%(datetime.datetime.fromtimestamp(process_start_01).isoformat() ))
	
	curr_time = time.mktime(datetime.datetime.now().timetuple())
	if curr_time > process_start_01:
		OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_01-5,process_start_01+(curr_time-process_start_01),1)
		process_start_01=process_start_01 + curr_time
		process_init = time.mktime(now_date.replace(second=0).timetuple()) + 60
	time_delta = (process_init - time.mktime(datetime.datetime.now().timetuple()))
	logger.info('Next calculation starts in %f seconds'%time_delta)
	ohlc_scheduler.enter(time_delta,1,ohlc_process_01,(sch,))

def ohlc_process_05(sch):
	duration = 60 * 5
	now_date = datetime.datetime.now()
	process_init = time.mktime(now_date.replace(second=0).timetuple()) + duration
	process_start_05 = time.mktime(now_date.replace(second=0).timetuple()) - duration
	time_limit = duration
	print(time_limit)
	OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_05,process_start_05+time_limit,5)
	process_start_05 = process_start_05 + time_limit
	logger.info('Waiting for next ...%s'%(datetime.datetime.fromtimestamp(process_start_05).isoformat() ))
	
	curr_time = time.mktime(datetime.datetime.now().timetuple())
	if curr_time > process_start_05:
		OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_05-5,process_start_05+(curr_time-process_start_05),1)
		process_start_05=process_start_05 + curr_time
		process_init = time.mktime(now_date.replace(second=0).timetuple()) + 60
	time_delta = (process_init - time.mktime(datetime.datetime.now().timetuple()))
	logger.info('Next calculation starts in %f seconds'%time_delta)
	ohlc_scheduler.enter(time_delta,1,ohlc_process_05,(sch,))

# Initializing one min ohlc
zeroth_sec = time.mktime(datetime.datetime.now().replace(second=0).timetuple()) + 60
print('To be initiated 1M at %s'%(datetime.datetime.fromtimestamp(zeroth_sec).isoformat()))
curr_time = time.mktime(datetime.datetime.now().timetuple())

zeroth_sec_05 = time.mktime(datetime.datetime.now().replace(second=0).timetuple()) + (60*5)
delta_5min = zeroth_sec_05 % (60*5)
zeroth_sec_05 = zeroth_sec_05 - delta_5min

print('05: Remaining: ',delta_5min, zeroth_sec_05)
print('To be initiated 5M at %s'%(datetime.datetime.fromtimestamp(zeroth_sec_05).isoformat()))

ohlc_scheduler.enter(zeroth_sec-curr_time,1,ohlc_process_01,(ohlc_scheduler,))
ohlc_scheduler.enter(zeroth_sec-curr_time,1,ohlc_process_05,(ohlc_scheduler,))
ohlc_scheduler.run()

def eod_calc():
	process_start_01 = time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day -2, 9, 37, 0).timetuple())
	day_end = time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day -2, 19, 45, 0).timetuple())
	while process_start_01 < day_end:
		time_limit = 60
		logger.info('Processing ...%s'%(datetime.datetime.fromtimestamp(process_start_01).isoformat() ))
		OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_01,process_start_01+time_limit,1)
		process_start_01 = process_start_01 + time_limit

def eod_calc_5():
	process_start_01 = time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day-2, 9, 0, 0).timetuple())
	day_end = time.mktime(datetime.datetime(today_date.year, today_date.month, today_date.day-2,10, 45, 0).timetuple())
	# topics = ['218567']
	while process_start_01 < day_end:
		time_limit = 60  * 5
		logger.info('Processing ...%s'%(datetime.datetime.fromtimestamp(process_start_01).isoformat() ))
		OHLCProcessor().process_all_from_cache_with_limit(topics,process_start_01,process_start_01+time_limit,5)
		process_start_01 = process_start_01 + time_limit

# eod_calc()
# eod_calc_5()

