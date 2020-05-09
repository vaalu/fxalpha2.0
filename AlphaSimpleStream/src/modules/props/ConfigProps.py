#!/usr/bin/env python3
import json
import configparser
import logging
import logging.handlers as handlers

print('Fetching access token from alice blue ant API')
config = configparser.ConfigParser()
config.read('application.config.properties')

# alphavantage.key=5U19TJGGJJNLYEIR
# alphavantage.url=https://www.alphavantage.co

AppProperties = {
	'COMMODITIES_MCX': json.loads(config.get('TRADING_INSTRUMENTS', 'instruments.commodities')),
	'ALPHAVANTAGE_KEY':config.get('TRADING_INSTRUMENTS', 'alphavantage.key'), 
	'ALPHAVANTAGE_URL':config.get('TRADING_INSTRUMENTS', 'alphavantage.url'), 
	'NIFTY50_URL':config.get('TRADING_INSTRUMENTS', 'nifty50.url'), 
	'KAFKA_URL':config.get('KAFKA', 'kafka.server.url'), 
	'KAFKA_PORT':config.get('KAFKA', 'kafka.server.port'), 
	'SOLR_PATH':config.get('SOLR', 'solr.server.path'),
	'SOLR_URL':config.get('SOLR', 'solr.server.url'), 
	'SOLR_PORT':config.get('SOLR', 'solr.server.port'), 
	'LOG_FILE':config.get('LOGGER', 'logging.file'),
	'LOG_LEVEL':config.get('LOGGER', 'logging.level')
}

log_level = {
	"info":logging.INFO, 
	"error":logging.ERROR, 
	"debug":logging.DEBUG, 
	"critical":logging.CRITICAL, 
	"fatal":logging.FATAL, 
	"console":logging.INFO
}

log_level_config = AppProperties['LOG_LEVEL']
default_log_level = log_level["info"]

if log_level_config != None:
	default_log_level = log_level[log_level_config.lower()]

logging.basicConfig( format='%(asctime)s : %(levelname)s : %(name)s : %(message)s', 
					level=default_log_level )
logging.log(logging.DEBUG, 'Starting logger')

app_logger = logging.getLogger('app_logger')
app_logger.setLevel(default_log_level)

rotating_handler = handlers.RotatingFileHandler(AppProperties['LOG_FILE'], maxBytes=50000000, backupCount=20)
app_logger.addHandler(rotating_handler)

class AppLogger():
	def debug(self, msg):
		app_logger.debug(msg)
		if log_level_config.lower() == "console":
			print(msg)
	def error(self, msg):
		app_logger.error(msg)
		if log_level_config.lower() == "console":
			print(msg)
	def critical(self, msg):
		app_logger.critical(msg)
		if log_level_config.lower() == "console":
			print(msg)
	def fatal(self, msg):
		app_logger.fatal(msg)
		if log_level_config.lower() == "console":
			print(msg)
	def info(self, msg):
		app_logger.info(msg)
		if log_level_config.lower() == "console":
			print(msg)

InstrumentMapper = {
	"15083":"ADANIPORTS",
	"217636":"ALUMINIUM",
	"236":"ASIANPAINT",
	"5900":"AXISBANK",
	"16669":"BAJAJ-AUTO",
	"16675":"BAJAJFINSV",
	"317":"BAJFINANCE",
	"10604":"BHARTIARTL",
	"526":"BPCL",
	"547":"BRITANNIA",
	"694":"CIPLA",
	"20374":"COALINDIA",
	"217649":"COPPER",
	"217322":"CRUDEOIL",
	"881":"DRREDDY",
	"910":"EICHERMOT",
	"4717":"GAIL",
	"1232":"GRASIM",
	"7229":"HCLTECH",
	"1330":"HDFC",
	"1333":"HDFCBANK",
	"1348":"HEROMOTOCO",
	"1363":"HINDALCO",
	"1394":"HINDUNILVR",
	"4963":"ICICIBANK",
	"5258":"INDUSINDBK",
	"29135":"INFRATEL",
	"1594":"INFY",
	"1624":"IOC",
	"1660":"ITC",
	"11723":"JSWSTEEL",
	"1922":"KOTAKBANK",
	"0":"LEAD",
	"11483":"LT",
	"2031":"M",
	"10999":"MARUTI",
	"218567":"NATURALGAS",
	"17963":"NESTLEIND",
	"217648":"NICKEL",
	"11630":"NTPC",
	"2475":"ONGC",
	"14977":"POWERGRID",
	"2885":"RELIANCE",
	"3045":"SBIN",
	"3103":"SHREECEM",
	"214542":"SILVER",
	"3351":"SUNPHARMA",
	"3456":"TATAMOTORS",
	"3499":"TATASTEEL",
	"11536":"TCS",
	"13538":"TECHM",
	"3506":"TITAN",
	"11532":"ULTRACEMCO",
	"11287":"UPL",
	"3063":"VEDL",
	"3787":"WIPRO",
	"3812":"ZEEL",
	"217635":"ZINC", 
	
	"ADANIPORTS":"15083",
	"ALUMINIUM":"217636",
	"ASIANPAINT":"236",
	"AXISBANK":"5900",
	"BAJAJ-AUTO":"16669",
	"BAJAJFINSV":"16675",
	"BAJFINANCE":"317",
	"BHARTIARTL":"10604",
	"BPCL":"526",
	"BRITANNIA":"547",
	"CIPLA":"694",
	"COALINDIA":"20374",
	"COPPER":"217649",
	"CRUDEOIL":"217322",
	"DRREDDY":"881",
	"EICHERMOT":"910",
	"GAIL":"4717",
	"GRASIM":"1232",
	"HCLTECH":"7229",
	"HDFC":"1330",
	"HDFCBANK":"1333",
	"HEROMOTOCO":"1348",
	"HINDALCO":"1363",
	"HINDUNILVR":"1394",
	"ICICIBANK":"4963",
	"INDUSINDBK":"5258",
	"INFRATEL":"29135",
	"INFY":"1594",
	"IOC":"1624",
	"ITC":"1660",
	"JSWSTEEL":"11723",
	"KOTAKBANK":"1922",
	"LEAD":"0",
	"LT":"11483",
	"M":"2031",
	"MARUTI":"10999",
	"NATURALGAS":"218567",
	"NESTLEIND":"17963",
	"NICKEL":"217648",
	"NTPC":"11630",
	"ONGC":"2475",
	"POWERGRID":"14977",
	"RELIANCE":"2885",
	"SBIN":"3045",
	"SHREECEM":"3103",
	"SILVER":"214542",
	"SUNPHARMA":"3351",
	"TATAMOTORS":"3456",
	"TATASTEEL":"3499",
	"TCS":"11536",
	"TECHM":"13538",
	"TITAN":"3506",
	"ULTRACEMCO":"11532",
	"UPL":"11287",
	"VEDL":"3063",
	"WIPRO":"3787",
	"ZEEL":"3812",
	"ZINC":"217635"
}
