import json
from datetime import datetime
from kafka import KafkaProducer
from modules.props.ConfigProps import aliceAnt, AppLogger

logger = AppLogger()
def dateconverter(o):
    if isinstance(o, datetime):
        return o.__str__()
kafka_server = '%s:%s'%(aliceAnt['KAFKA_URL'], aliceAnt['KAFKA_PORT'])
producer = KafkaProducer(bootstrap_servers=kafka_server, value_serializer=lambda v: json.dumps(v, default=dateconverter).encode('utf-8'))

class KafkaUtil():
	def __init__(self):
		logger.info('Initializing kafka util')
	def post_instruments(self, instruments):
		for instrument in instruments:
			logger.info('Instrument: %s'%str(instrument))
			producer.send('INSTRUMENTS', instrument)
			producer.flush()