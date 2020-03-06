import { Injectable, ProviderScope } from '@graphql-modules/di'
import csv from 'csvtojson'
import 'dotenv-safe/config'

@Injectable({
	scope:ProviderScope.Session
})
export default class TradingScrips {
	public async getScrips() {
		return allEquities
	}

	public async getForSymbol(filter?:any) {
		const equities:any = await allEquities.then(jsonArr => jsonArr)
		const equitiesData:any = await equities.find( (equityObj:any) => ((equityObj.symbol === filter.symbol) && (equityObj.segment === 'NSE') && (equityObj.exchange === 'NSE')))
		return equitiesData ? equitiesData : []
	}
}

const fetchCsvData = async () => {

	const csvPath = './static-data/equities.csv'
	let equitiesData:any = []

	await csv({
		headers:[	
			"instrument_id", 
			"exchange_token", 
			"symbol", 
			"company", 
			"last_price", 
			"expiry", 
			"strike", 
			"tick_size", 
			"lot_size", 
			"instrument_type", 
			"segment", 
			"exchange"
		]
	}).fromFile(csvPath)
	.on('json', (jsonObj) => {
		return {
			company : jsonObj.company,
			exchange: jsonObj.exchange,
			exchange_token : jsonObj.exchange_token, 
			instrument_id : jsonObj.instrument_id,  
			segment: jsonObj.segment,
			symbol : jsonObj.symbol, 
		}
	})
	.then((jsonObj) => {
		equitiesData = jsonObj
	})
	const deDuplicatedData = [...new Set(equitiesData.map((obj:any) => JSON.stringify(obj)))].map((str:any) => JSON.parse(str))
	return deDuplicatedData
}
const allEquities = fetchCsvData()

