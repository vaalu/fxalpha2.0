from kafka import KafkaConsumer
from modules.props.ConfigProps import AppProperties, AppLogger
from modules.util.DefaultMessageHandlerLegacy import DefaultMessageHandlerLegacy
from modules.util.OHLCSingleItemProcessor import OHLCSingleItemProcessor
from collections import deque
logger = AppLogger()

class AlphaConsumerLegacy():
	kafka_server = '%s:%s'%(AppProperties['KAFKA_URL'], AppProperties['KAFKA_PORT'])
	init_consumer = KafkaConsumer(	bootstrap_servers=[kafka_server], 
								api_version=(0, 10), 
								consumer_timeout_ms=1000)
	topics = init_consumer.topics()
	logger.info('All topics that are present: ')
	logger.info(topics)
	consumer = KafkaConsumer(	*topics, 
								auto_offset_reset='latest',
								bootstrap_servers=[kafka_server], 
								api_version=(0, 10), 
								consumer_timeout_ms=1000)
	
	handler = DefaultMessageHandlerLegacy()
	__ohlc_handlers = {}
	def __init__(self):
		logger.info('Initializing kafka consumer with all topics')
	def __fetch_config(self):
		return self.topics, self.consumer
	def consume_messages(self):
		while True:
			for msg in self.consumer:
				self.handler.handle(msg)
