import { Injectable, ProviderScope } from '@graphql-modules/di'
import csv from 'csvtojson'
import 'dotenv-safe/config'
import fetch from 'node-fetch'
import TradingScrips from './static-trading-scrips'


@Injectable({
	scope:ProviderScope.Session
})

export default class Nifty50 {
	
	public getScrips = async () => {
		const NIFTY_50_URL = process.env.NIFTY50_URL
		console.log(`Fetching Nifty 50 List from ${NIFTY_50_URL}`)
		const nifty50Data:any = await fetch(NIFTY_50_URL!)
								.then( res => res.text() )
								.then( body => csv({
									headers:["company", "industry", "symbol", "series", "isin"]
								}).fromString(body).subscribe((jsonObj) => {
									jsonObj.date = (new Date()).toISOString().slice(0, 10) 
									return jsonObj
								}))

		let niftyResult = {
			count:0,
			scrips:[]
		}
		if(nifty50Data) {
			niftyResult = {
				count:nifty50Data.length, 
				scrips:nifty50Data
			}
		}
		return niftyResult
	} 
	public getNifty50Sourced = async () => {
		const niftyScrips = await this.getScrips()
		
		const niftyData:any = new Array()
		const tscripts = new TradingScrips()
		const allScrips = await tscripts.getScrips()

		niftyScrips.scrips.forEach((element:any) => {
			const dateVal = (new Date()).toISOString().slice(0, 10) 
			element.date = dateVal
			
			const zId = allScrips.find(elem => {
				if((elem.symbol === element.symbol) && (elem.segment === 'NSE') && (elem.exchange === 'NSE')) {
					return elem.instrument_id
				}})
			Object.assign(element, {
				date:dateVal,
				exchange_token:zId.exchange_token, 
				instrument_id:zId.instrument_id
			}) 
			// console.log('Element pushed: ', element)
			niftyData.push(element)

		});
		
		// console.log('Nifty 50 Data: ', niftyData)
		let niftyResult = {
			count:0,
			scrips:[]
		}
		if(niftyData) {
			niftyResult = {
				count:niftyData.length, 
				scrips:niftyData
			}
		}
		return niftyResult
	}

}
