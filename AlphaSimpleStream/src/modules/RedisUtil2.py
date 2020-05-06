import redis
import json
import redis
from modules.props.ConfigProps import AppProperties, AppLogger, InstrumentMapper
from modules.util.SolrMessageHandler import SolrMessageHandler
from modules.Nifty50Instruments import Nifty50

logger = AppLogger()

class RedisUtil2():
	__red = redis.Redis(host='localhost', port=6379)
	__mapper = InstrumentMapper
	__handlers = {}
	__core_id=''
	__instruments = list([])
	def __init__(self, instrument_id):
		print('Default redis util')
		self.__instrument_id=instrument_id
		self.__core_id=self.__mapper[instrument_id]
		self.__handlers[self.__core_id] = SolrMessageHandler(self.__core_id)
	
	def readForInstrument(self):
		print('Reading instrument %s'%(self.__instrument_id))
		instr = '%s:*'%(self.__instrument_id)
		keys = self.__red.keys(instr)
		for key in keys:
			core = self.__red.hget(key, 'instrument_token')
			exchange_timestamp= self.__red.hget(key, 'exchange_timestamp')
			instrument_token= self.__red.hget(key, 'instrument_token')
			last_traded_price= self.__red.hget(key, 'last_traded_price')
			last_traded_time= self.__red.hget(key, 'last_traded_time')
			last_traded_quantity= self.__red.hget(key, 'last_traded_quantity')
			trade_volume= self.__red.hget(key, 'trade_volume')
			best_bid_price= self.__red.hget(key, 'best_bid_price')
			best_bid_quantity= self.__red.hget(key, 'best_bid_quantity')
			best_ask_price= self.__red.hget(key, 'best_ask_price')
			best_ask_quantity= self.__red.hget(key, 'best_ask_quantity')
			total_buy_quantity= self.__red.hget(key, 'total_buy_quantity')
			total_sell_quantity= self.__red.hget(key, 'total_sell_quantity')
			average_trade_price= self.__red.hget(key, 'average_trade_price')
			open_price= self.__red.hget(key, 'open_price')
			high_price= self.__red.hget(key, 'high_price')
			low_price= self.__red.hget(key, 'low_price')
			close_price= self.__red.hget(key, 'close_price')
			yearly_high_price= self.__red.hget(key, 'yearly_high_price')
			yearly_low_price= self.__red.hget(key, 'yearly_low_price')
		
			solr_doc = {
				'exchange_timestamp':exchange_timestamp.decode('utf-8'), 
				'instrument_token':instrument_token.decode('utf-8'), 
				'instrument':self.__mapper[instrument_token.decode('utf-8')], 
				'last_traded_price':last_traded_price.decode('utf-8'), 
				'last_traded_time':last_traded_time.decode('utf-8'), 
				'last_traded_quantity':last_traded_quantity.decode('utf-8'), 
				'trade_volume':trade_volume.decode('utf-8'), 
				'best_bid_price':best_bid_price.decode('utf-8'), 
				'best_bid_quantity':best_bid_quantity.decode('utf-8'), 
				'best_ask_price':best_ask_price.decode('utf-8'), 
				'best_ask_quantity':best_ask_quantity.decode('utf-8'), 
				'total_buy_quantity':total_buy_quantity.decode('utf-8'), 
				'total_sell_quantity':total_sell_quantity.decode('utf-8'), 
				'average_trade_price':average_trade_price.decode('utf-8'), 
				'open_price':open_price.decode('utf-8'), 
				'high_price':high_price.decode('utf-8'), 
				'low_price':low_price.decode('utf-8'), 
				'close_price':close_price.decode('utf-8'), 
				'yearly_high_price':yearly_high_price.decode('utf-8'), 
				'yearly_low_price':yearly_low_price.decode('utf-8')
			}
			self.__handlers[self.__core_id].process_item(solr_doc)
		self.__handlers[self.__core_id].process_final_chunks()
