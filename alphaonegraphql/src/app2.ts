import { ApolloServer, gql } from 'apollo-server-express'
import cors from 'cors'
import express from 'express'
import { mergeSchemas } from 'graphql-tools'
import AppModule from './modules'

const APOLLO_INTROSPECTION = process.env.APOLLO_INTROSPECTION === "true"
const APOLLO_PLAYGROUND = process.env.APOLLO_PLAYGROUND === "true"
const APOLLO_DEBUG = process.env.APOLLO_DEBUG === "true"
const { context, schema } = AppModule;

const app = express()
const server = new ApolloServer({
	context, 
	debug:APOLLO_DEBUG, 
	introspection:APOLLO_INTROSPECTION, 
	playground:APOLLO_PLAYGROUND, 
	schema:mergeSchemas({
		schemas: [ schema ]
	}), 
	
})
server.applyMiddleware({app})
app.listen({port:4000}, () => {
	console.log('Apollo GraphQL server running in http://localhost:4000/')
})









