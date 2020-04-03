import { GraphQLModule } from '@graphql-modules/core';
import { importSchema } from 'graphql-import'
import { Commodities } from '../../datasources'
import resolvers from './resolvers';

const typeDefs = importSchema('./src/modules/commodities/schema.graphql')
const CommoditiesScrips = new GraphQLModule({
	providers:[Commodities], 
	resolverValidationOptions:{
		requireResolversForResolveType:false
	}, 
	resolvers,
	typeDefs	
});

export default CommoditiesScrips;