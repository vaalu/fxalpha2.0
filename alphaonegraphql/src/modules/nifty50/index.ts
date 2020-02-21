import { GraphQLModule } from '@graphql-modules/core';
import { importSchema } from 'graphql-import'
import { Nifty50 } from '../../datasources'
import resolvers from './resolvers';

const typeDefs = importSchema('./src/modules/nifty50/schema.graphql')
const Nifty50Stocks = new GraphQLModule({
	providers:[Nifty50], 
	resolverValidationOptions:{
		requireResolversForResolveType:false
	}, 
	resolvers,
	typeDefs	
});

export default Nifty50Stocks;