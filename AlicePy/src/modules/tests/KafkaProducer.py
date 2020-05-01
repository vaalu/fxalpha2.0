import json
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
# producer.send('sample', b'Hello, World!')
# producer.send('sample', key=b'message-two', value=b'This is Kafka-Python')
# datum = {'foo-1': 'bar--2'}
producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
datum = {'instrument_token': 16675, 'last_traded_price': 510435.0, 'last_traded_time': 1588242551, 'last_traded_quantity': 4, 'trade_volume': 1064409, 'best_bid_price': 510435.0, 'best_bid_quantity': 462, 'best_ask_price': 0.0, 'best_ask_quantity': 0, 'total_buy_quantity': 462, 'total_sell_quantity': 0, 'average_trade_price': 512460.0, 'exchange_timestamp': 1588242551, 'open_price': 510800.0, 'high_price': 517500.0, 'low_price': 505085.0, 'close_price': 499865.0, 'yearly_high_price': 995000.0, 'yearly_low_price': 416025.0}
producer.send('16675', datum)

# producer.flush()