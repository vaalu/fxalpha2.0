from kafka import KafkaConsumer
from modules.util.DefaultMessageHandler import DefaultMessageHandler
from modules.props.ConfigProps import aliceAnt, AppLogger

logger = AppLogger()

class AlphaConsumer():
	topics=list(['13538', '16675', '2031', '1660', '1594', '10999', '526', '218567', '3045', '3812', '1624', '1922', '4717', '1232', '1363', '910', '236', '694', '3351', '2885', '3499', '5258', '3103', '1348', '5900', '11483', '3063', '11723', '10604', '16669', '317', '881', '3456', '1330', '1394', '17963', '11630', '29135', '4963', '3506', '2475', '11532', '7229', '1333', '11536', '15083', '11287', '547', '20374', '3787', '14977'])
	kafka_server = '%s:%s'%(aliceAnt['KAFKA_URL'], aliceAnt['KAFKA_PORT'])
	consumer = KafkaConsumer(	*topics, 
								auto_offset_reset='earliest',
								bootstrap_servers=[kafka_server], 
								api_version=(0, 10), 
								consumer_timeout_ms=1000)
	handler = DefaultMessageHandler()
	def __init__(self):
		logger.info('Initializing kafka consumer with all topics')
	def __fetch_config(self):
		return self.topics, self.consumer
	def consume_messages(self):
		while True:
			for msg in self.consumer:
				self.handler.handle(msg)


