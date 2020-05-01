import json
import redis
from kafka import KafkaConsumer
# topics=list(['13538', '16675', '2031', '1660', '1594', '10999', '526', '218567', '3045', '3812', '1624', '1922', '4717', '1232', '1363', '910', '236', '694', '3351', '2885', '3499', '5258', '3103', '1348', '5900', '11483', '3063', '11723', '10604', '16669', '317', '881', '3456', '1330', '1394', '17963', '11630', '29135', '4963', '3506', '2475', '11532', '7229', '1333', '11536', '15083', '11287', '547', '20374', '3787', '14977'])
topics=list(['13538', '16675'])

r = redis.Redis(host='localhost', port=6379)

def process_13538(msg):
	print('Processing TECHM %s'%(msg.topic))
def process_16675(msg):
	print('Processing BAJAJFINSV %s'%(msg.topic))

tfunctions = {
	'13538':process_13538, '16675': process_16675
}
consumer = KafkaConsumer(	'218567', 
							auto_offset_reset='latest',
                            bootstrap_servers=['localhost:9092'], 
							api_version=(0, 10), 
							consumer_timeout_ms=1000)
while True:
	for msg in consumer:
		# tfunctions[msg.topic](msg)
		source_val = json.loads(msg.value)
		hset_key = '%s:%s'%(msg.topic, source_val["exchange_timestamp"])
		print(hset_key)
		r.hset(hset_key, "exchange_timestamp", source_val["exchange_timestamp"])
		r.hset(hset_key, "instrument_token", source_val["instrument_token"])
		r.hset(hset_key, "last_traded_price", source_val["last_traded_price"])
		r.hset(hset_key, "last_traded_time", source_val["last_traded_time"])
		r.hset(hset_key, "last_traded_quantity", source_val["last_traded_quantity"])
		r.hset(hset_key, "trade_volume", source_val["trade_volume"])
		r.hset(hset_key, "best_bid_price", source_val["best_bid_price"])
		r.hset(hset_key, "best_bid_quantity", source_val["best_bid_quantity"])
		r.hset(hset_key, "best_ask_price", source_val["best_ask_price"])
		r.hset(hset_key, "best_ask_quantity", source_val["best_ask_quantity"])
		r.hset(hset_key, "total_buy_quantity", source_val["total_buy_quantity"])
		r.hset(hset_key, "total_sell_quantity", source_val["total_sell_quantity"])
		r.hset(hset_key, "average_trade_price", source_val["average_trade_price"])
		r.hset(hset_key, "exchange_timestamp", source_val["exchange_timestamp"])
		r.hset(hset_key, "open_price", source_val["open_price"])
		r.hset(hset_key, "high_price", source_val["high_price"])
		r.hset(hset_key, "low_price", source_val["low_price"])
		r.hset(hset_key, "close_price", source_val["close_price"])
		r.hset(hset_key, "yearly_high_price", source_val["yearly_high_price"])
		r.hset(hset_key, "yearly_low_price", source_val["yearly_low_price"])
if consumer is not None:
	consumer.close()
print('Kafka subscription to topic - end.')