import json
from kafka import KafkaConsumer
from modules.props.ConfigProps import AppLogger, AppProperties

logger = AppLogger()
class KafkaUtil():
	__instr_topics = ['INSTRUMENTS_EQUITIES','INSTRUMENTS_COMMODITIES']
	__kafka_server = '%s:%s'%(AppProperties['KAFKA_URL'], AppProperties['KAFKA_PORT'])
	__init_consumer = KafkaConsumer(	*__instr_topics, 
								auto_offset_reset='earliest',
								bootstrap_servers=[__kafka_server], 
								api_version=(0, 10), 
								consumer_timeout_ms=1000)
	__topics = set([])
	__commodities = set([])
	__equities = set([])
	__mapped_instruments = {}
	def __init__(self):
		for msg in self.__init_consumer:
			value = json.loads(msg.value)
			logger.info(value)
			if value["exchange"] == 'MCX':
				self.__commodities.add(str(value["token"]))
			else:
				self.__equities.add(str(value["token"]))
			self.__topics.add(str(value["token"]))
			self.__mapped_instruments[str(value["token"])]=str(value["symbol"])
		if self.__init_consumer is not None:
			self.__init_consumer.close()
	def fetch_all_instruments_with_info(self):
		return self.__mapped_instruments
	def fetch_instruments_all(self):
		return list(self.__topics)
	def fetch_instruments_equities(self):
		return list(self.__equities)
	def fetch_instruments_commodities(self):
		return list(self.__commodities)