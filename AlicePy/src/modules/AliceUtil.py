#!/usr/bin/env python3
import configparser
from alice_blue import *
import logging 

def logger(message):
	logging.log(logging.DEBUG, message)

config = configparser.ConfigParser()
config.read('application.config.properties')

aliceAnt = {
	'CLIENT_USER' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.user'), 
	'CLIENT_SECRET' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.secret'), 
	'CLIENT_PASSWORD' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.password')
}

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
			logger('Token file does not exist')
		return alice_token

	def rewriteToken(self, token):
		# logger('Token obtained %s'%(token))
		try:
			with open('alice.token', 'w') as file:
				file.write(token)
				file.close()
		except:
			logger('Unable to create token file')

	def fetchTokenIfNotExists(self):
		alice_token = self.fetchTokenFromFile()
		# logger('Token fetched: %s'%(alice_token))
		try:
			logger('Checking access token')
			alice = AliceBlue(	username=aliceAnt['CLIENT_USER'], 
								password=aliceAnt['CLIENT_PASSWORD'], 
								access_token=alice_token, 
								master_contracts_to_download=['NSE', 'MCX'])
			logger('Valid access token')
		except:
			self.retry_count=self.retry_count+1
			if self.retry_count < 5:
				logger('Invalid access token. Retrying %i'%(self.retry_count))
				alice_token = AliceBlue.login_and_get_access_token(	username=aliceAnt['CLIENT_USER'], 
																		password=aliceAnt['CLIENT_PASSWORD'], 
																		twoFA='1',  
																		api_secret=aliceAnt['CLIENT_SECRET'])
				if alice_token != '':
					self.rewriteToken(alice_token)
					self.fetchTokenIfNotExists()
			else: 
				logger('Unable to get new token. Abandoning request.')
			
		finally:
			logger('Token obtained...')
		return alice_token