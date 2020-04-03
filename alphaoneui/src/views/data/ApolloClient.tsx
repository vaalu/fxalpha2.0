import ApolloClient from 'apollo-boost'
import { APOLLO_SERVER } from '../../AppConstants'

export default new ApolloClient ({
	uri: APOLLO_SERVER
})