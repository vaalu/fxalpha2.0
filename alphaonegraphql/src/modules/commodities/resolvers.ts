import { Commodities } from '../../datasources'

export default {

	Query: {
		getCommodities : async () => {
			const commodities = new Commodities()
			const response = commodities.getCommoditiesScrips()
			const commItems = {
				count:0,
				scrips:[]
			}
			response.then((item:any) => {
				if(item) {
					commItems.count = item.length,
					commItems.scrips = item
				}
			})
			return await commItems
		}
	}

}