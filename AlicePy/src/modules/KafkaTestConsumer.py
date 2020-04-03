import json
from kafka import KafkaConsumer
topic_name='3499'
consumer = KafkaConsumer(	topic_name, 
							auto_offset_reset='latest',
                            bootstrap_servers=['localhost:9092'], 
							api_version=(0, 10), 
							consumer_timeout_ms=1000)
while True:
	for msg in consumer:
		print('Message from topic %s - %s'%(topic_name, msg.value))
if consumer is not None:
	consumer.close()
print('Kafka subscription to topic - end.')