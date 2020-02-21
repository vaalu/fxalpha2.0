import { Injectable, ProviderScope } from '@graphql-modules/di'
import csv from 'csvtojson'
import 'dotenv-safe/config'
import fetch from 'node-fetch'


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

}
