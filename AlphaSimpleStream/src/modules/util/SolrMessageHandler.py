import json
import pysolr
from collections import deque

from modules.props.ConfigProps import AppLogger, AppProperties
logger = AppLogger()

class SolrMessageHandler():
	__solr_server_url = 'http://%s:%s/solr/'%(AppProperties['SOLR_URL'], AppProperties['SOLR_PORT'])
	__docs = deque()
	__chunk = list([])
	__start_indexing = False
	solr = {}
	def __init__(self, solr_core):
		solr_url = '%s%s/update/json?commit=true'%(self.__solr_server_url, solr_core)
		logger.info('Default processing for solr for core: %s'%(solr_core))
		self.solr = {
			'server':pysolr.Solr(solr_url),
			'url':solr_url
		}
	def start_indexing_docs(self):
		if len(self.__docs) > 0 and self.__start_indexing:
			logger.debug('Length of docs: %i, indexing start: %s'%(len(self.__docs), self.__start_indexing))
			solr_doc = self.__docs.pop()
			if solr_doc != None:
				print(self.solr['url'])
				self.solr['server'].add(solr_doc)

	def process_item(self, rmsg):
		if len(self.__chunk) > 999:
			self.__docs.append(self.__chunk)
			self.__chunk = list([])
			self.start_indexing_docs()
		self.__chunk.append(rmsg)
		self.__start_indexing = True
	
	def process_final_chunks(self):
		if len(self.__chunk) > 0:
			self.__docs.append(self.__chunk)
			self.start_indexing_docs()
			self.__start_indexing = True
			logger.debug('Indexing final chunks...%s'%(self.solr['url']))
			while len(self.__docs) > 0:
				self.start_indexing_docs()
