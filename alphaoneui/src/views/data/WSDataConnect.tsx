import gql from "graphql-tag";
import ApolloClient from './ApolloClient'
let data:any = []
export default async (token:string) => {
	
	await ApolloClient.query({
		query : GET_COMMODITIES_QUERY, 
		variables : {token}
	}).then(result => {
		data = result.data
	})
	return data.aliceAntCommodityScrips
} 

const GET_COMMODITIES_QUERY = gql`
		query ($token:String!){
			aliceConnect(token:$token) {
				info
			}
		}
	`