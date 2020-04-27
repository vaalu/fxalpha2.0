import { Injectable, ProviderScope } from '@graphql-modules/di'
// import ab2str from 'arraybuffer-to-string'
import 'dotenv-safe/config'
import fetch from 'node-fetch'

@Injectable({
	scope:ProviderScope.Session
})

export default class AliceConnect {
	public getProfile = () => {
		console.log('Profile information is being fetched.')
		
		return {
			info:'Profile information is being fetched.'
		}
	}
	public connect = () => {
		console.log('Connecting to alice ant.')
		const wsUtilityUrl = process.env.ALICE_WS_UTILITY_URL + '/instruments'
		console.log('Establishinig websocket url connection with alice utility: ', wsUtilityUrl)
		
		fetch(wsUtilityUrl!)
			.then( res => res.text() )
			.then(body => {
				console.log('Result from the ws utility: ', body)
			})
		return {
			info:'Alice ant connected.'
		}
	}
	public connectLegacy = (token:string) => {
		console.log('Connecting to alice ant.', token)
		const wsUtilityUrl = process.env.ALICE_WS_UTILITY_URL + '/' + token
		console.log('Establishinig websocket url connection with alice utility: ', wsUtilityUrl)
		
		fetch(wsUtilityUrl!)
			.then( res => res.text() )
			.then(body => {
				console.log('Result from the ws utility: ', body)
			})
		return {
			info:'Alice ant connected.'
		}
	}
}