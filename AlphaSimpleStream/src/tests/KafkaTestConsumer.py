import pysolr
import json
# import requests
from kafka import KafkaConsumer
import concurrent.futures
import redis
try:
	import thread
except ImportError:
	import _thread as thread
import time

class AliceStream():
	r = redis.Redis(host='localhost', port=6379)
	consumer = KafkaConsumer(	topic_name, 
								auto_offset_reset='earliest',
								bootstrap_servers=['localhost:9092'], 
								api_version=(0, 10), 
								consumer_timeout_ms=1000)
	

topic_name='236'
while True:
	for msg in consumer:
		source_val = json.loads(msg.value)
		hset_key = 'ASIANPAINT:%s'%(source_val["exchange_timestamp"])
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
		# def asyncPost(source_val):
		#	print(source_val)
		# thread.start_new_thread(asyncPost, ())
		# with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
		# 	source_val = json.loads(msg.value)
		# 	executor.submit(asyncPost, source_val)
		# print('Message from topic %s - %s'%(topic_name, msg.value))
		# requests.post('http://mohu.local:8983/solr/natgas/update?wt=json', data=json.loads(msg.value))
if consumer is not None:
	consumer.close()
print('Kafka subscription to topic - end.')