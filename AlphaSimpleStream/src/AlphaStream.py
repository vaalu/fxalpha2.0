import time
from modules.props.ConfigProps import AppLogger, AppProperties
from modules.OHLCProcessor import OHLCProcessor
from kafka import KafkaConsumer

logger = AppLogger()

# ohlc_scheduler = sched.scheduler(time.time, time.sleep)

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
	def process_stream(self):
		curr_time = 1589259480
		logger.info('Started processing streams...until %f'%(curr_time) )
		self.ohlc_processor.process_all_from_cache(self.topics, curr_time)
		# self.ohlc_processor.read_from_cache(['218567'], curr_time)

AlphaStream().process_stream()
# def ohlc_process(sch):
# 	print(sch.now().time())
# 	ohlc_scheduler.enter(60,1,ohlc_process,(sch,))
# ohlc_scheduler.enter(60,1,ohlc_process,(ohlc_scheduler,))
# ohlc_scheduler.run()