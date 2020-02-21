import { GraphQLModule } from '@graphql-modules/core';
import 'graphql-import-node';
import 'reflect-metadata';

import CommoditiesScrips from './commodities'
import Nifty50Stocks from './nifty50'


const AppModule = new GraphQLModule({
	imports:[
		Nifty50Stocks, 
		CommoditiesScrips
	], 
	resolverValidationOptions : { requireResolversForResolveType:false }
});

export default AppModule;