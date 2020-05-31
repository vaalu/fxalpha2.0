#!/usr/bin/env python3
from modules.props.ConfigProps import AppLogger, AppProps
from alice_blue import *

logger = AppLogger()

class AliceUtil():
	retry_count = 0
	def fetchTokenFromFile(self):
		alice_token = ''
		try:
			with open('alice.token', 'r') as file:
				lines = file.readlines()
				for token in lines:
					alice_token = token
				file.close()
		except:
			logger.info('Token file does not exist')
		return alice_token

	def rewriteToken(self, token):
		# logger.info('Token obtained %s'%(token))
		try:
			with open('alice.token', 'w') as file:
				file.write(token)
				file.close()
		except:
			logger.info('Unable to create token file')

	def fetchTokenIfNotExists(self):
		alice_token = self.fetchTokenFromFile()
		# logger.info('Token fetched: %s'%(alice_token))
		try:
			logger.info('Checking access token')
			alice = AliceBlue(	username=AppProps['CLIENT_USER'], 
								password=AppProps['CLIENT_PASSWORD'], 
								access_token=alice_token, 
								master_contracts_to_download=['NSE', 'MCX'])
			logger.info('Valid access token')
		except:
			self.retry_count=self.retry_count+1
			if self.retry_count < 5:
				logger.info('Invalid access token. Retrying %i'%(self.retry_count))
				alice_token = AliceBlue.login_and_get_access_token(	username=AppProps['CLIENT_USER'], 
																		password=AppProps['CLIENT_PASSWORD'], 
																		twoFA='1',  
																		api_secret=AppProps['CLIENT_SECRET'])
				if alice_token != '':
					self.rewriteToken(alice_token)
					self.fetchTokenIfNotExists()
			else: 
				logger.info('Unable to get new token. Abandoning request.')
			
		finally:
			logger.info('Token obtained...')
		return alice_token