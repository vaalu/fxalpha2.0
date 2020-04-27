#!/usr/bin/env python3
import json
import configparser

print('Fetching access token from alice blue ant API')
config = configparser.ConfigParser()
config.read('application.config.properties')

# alphavantage.key=5U19TJGGJJNLYEIR
# alphavantage.url=https://www.alphavantage.co

aliceAnt = {
	'CLIENT_ID' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.id'), 
	'CLIENT_USER' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.user'), 
	'CLIENT_SECRET' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.secret'), 
	'CLIENT_PASSWORD' : config.get('ALICE_ANT_OAUTH2', 'alice.ant.client.password'), 
	'URL_AUTH' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.auth'), 
	'URL_TOKEN' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.token'), 
	'URL_CALLBACK' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.callback'), 
	'URL_LOGIN' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.login'),
	'URL_2FA' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.2fa'),
	'URL_WSS' : config.get('ALICE_ANT_SERVER', 'alice.ant.url.wss'), 
	'ALICE_API_BASE': config.get('ALICE_ANT_API', 'alice.ant.api.base'),
	'ALICE_PROFILE' : config.get('ALICE_ANT_API', 'alice.ant.api.profile'),
	'LEGACY_COMMODITIES':json.loads(config.get('TRADING_INSTRUMENTS', 'legacy.instruments.commodities')), 
	'ALPHAVANTAGE_KEY':config.get('TRADING_INSTRUMENTS', 'alphavantage.key'), 
	'ALPHAVANTAGE_URL':config.get('TRADING_INSTRUMENTS', 'alphavantage.url'), 
	'NIFTY50_URL':config.get('TRADING_INSTRUMENTS', 'nifty50.url')
}
