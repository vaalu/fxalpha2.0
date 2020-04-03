import { Nifty50 } from '../../datasources'

export default {

	Query: {
		getNifty50 : async () => {
			const nifty = new Nifty50()
			const response = nifty.getScrips()
			response.then((item:any) => {
				console.log('Data count: ', item.count)
			})
			// console.log(response)
			return response
		},
		getNifty50Sourced : async () => {
			const nifty = new Nifty50()
			const response = nifty.getNifty50Sourced()
			console.log(response)
			return response
		}
	}

}