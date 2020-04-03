import { GraphQLModule } from '@graphql-modules/core';
import { importSchema } from 'graphql-import';
import { AliceConnect } from '../../datasources';
import resolvers from './resolvers';

const typeDefs = importSchema('./src/modules/alice/schema.graphql')
const AliceAnt = new GraphQLModule({
	providers:[AliceConnect], 
	resolverValidationOptions:{
		requireResolversForResolveType:false
	}, 
	resolvers,
	typeDefs	
});

export default AliceAnt