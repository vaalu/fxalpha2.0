import os
import urllib 
import logging
from modules.props.ConfigProps import AppProperties, AppLogger
from modules.Nifty50Instruments import Nifty50

logger = AppLogger()

class SolrConfig():
	
	instruments=AppProperties['COMMODITIES_MCX']
	equities=Nifty50().fetchNifty50()
	command = '%s create_core -c'%(AppProperties['SOLR_PATH'])
	
	def log_message(self, message=''):
		logger.info(message)
		print(message)
	
	def create_samples(self):
		stream = os.popen('%s SAMPLE'%(self.command))
		self.log_message(stream.read())

		stream = os.popen('%s RAW'%(self.command))
		self.log_message(stream.read())

		stream = os.popen('%s TEST'%(self.command))
		self.log_message(stream.read())
	
	def create_cores_for_instruments(self):
		for instrument in self.instruments:
			create_core_command = '%s %s'%(self.command, instrument)
			stream = os.popen(create_core_command)
			self.log_message(stream.read())
		for equity in self.equities:
			create_core_command = '%s %s'%(self.command, equity)
			logger.debug(create_core_command)
			stream = os.popen(create_core_command)
			self.log_message(stream.read())