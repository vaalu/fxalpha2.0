import { Injectable, ProviderScope } from '@graphql-modules/di'
import csv from 'csvtojson'
import 'dotenv-safe/config'
import fetch from 'node-fetch'


@Injectable({
	scope:ProviderScope.Session
})

export default class Commodities {
	
	public getCommoditiesScrips = async () => {
		return [
			{'instrument':'Crude Oil', 'id':'CRUDEOIL', 'token':216824, 'date' : (new Date()).toISOString().slice(0, 10) }, 
			{'instrument':'Natural Gas', 'id':'NATURALGAS', 'token':217622, 'date' : (new Date()).toISOString().slice(0, 10)}
		]
	}

}
