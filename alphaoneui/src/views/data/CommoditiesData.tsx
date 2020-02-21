import gql from "graphql-tag";
import ApolloClient from './ApolloClient'
let data:any = []
export default async () => {
	
	await ApolloClient.query({
		query : GET_COMMODITIES_QUERY
	}).then(result => {
		data = result.data
	})
	return data.getCommodities.scrips
} 

const GET_COMMODITIES_QUERY = gql`
		query {
			getCommodities {
				scrips {
					instrument
					id
					token
				}
			}
		}
	`