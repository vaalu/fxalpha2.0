import gql from "graphql-tag";
import ApolloClient from './ApolloClient'
let data:any = []
export default async () => {
	// console.log('Nifty 50 Stocks: From ScriptsData()')
	await ApolloClient.query({
		query : GET_NIFTY_50_QUERY
	}).then(result => {
		// console.log('Resolved value: ', result)
		data = result.data.getNifty50
	})
	return data
} 

const GET_NIFTY_50_QUERY = gql`
		query {
				getNifty50 {
					count
					scrips {
						company
						industry
						symbol
						isin
						date
						series
					}
				}
			}`