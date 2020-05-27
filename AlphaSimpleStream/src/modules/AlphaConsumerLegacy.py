import json
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
	# logger.info('All topics that are present: ')
	topics = ['INSTRUMENTS_EQUITIES','INSTRUMENTS_COMMODITIES']
	logger.info('All topics that are present: %s'%str(topics))
	consumer = KafkaConsumer(	*topics, 
								auto_offset_reset='earliest',
								bootstrap_servers=[kafka_server], 
								api_version=(0, 10), 
								consumer_timeout_ms=1000)
	
	handler = DefaultMessageHandlerLegacy()
	__ohlc_handlers = {}
	def __init__(self):
		logger.info('Initializing kafka consumer with all topics') 
		topics = list([])
	def __fetch_config(self):
		commodities = list([])
		equities = list([])
		all_instruments = []
		for msg in self.consumer:
			value = json.loads(msg.value)
			if value["exchange"] == 'MCX':
				commodities.append(str(value["token"]))
			else:
				equities.append(str(value["token"]))
			all_instruments.append(str(value["token"]))
		if self.consumer is not None:
			self.consumer.close()
		kconsumer = KafkaConsumer(	*all_instruments, 
								auto_offset_reset='latest',
								bootstrap_servers=[self.kafka_server], 
								api_version=(0, 10), 
								consumer_timeout_ms=10000)
		# return self.topics, self.consumer
		return equities, commodities, kconsumer
	def init_config(self):
		self.__fetch_config()

	def consume_messages(self):
		equities, commodities, kconsumer = self.__fetch_config()
		while True:
			for msg in kconsumer:
				self.handler.handle(msg)
