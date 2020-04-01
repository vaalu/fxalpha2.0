import { ApolloServer, mergeSchemas } from 'apollo-server-express'
import 'dotenv-safe/config'
import express from 'express';
import AppModule from './modules';


const APOLLO_INTROSPECTION = process.env.APOLLO_INTROSPECTION === "true"
const APOLLO_PLAYGROUND = process.env.APOLLO_PLAYGROUND === "true"
const APOLLO_DEBUG = process.env.APOLLO_DEBUG === "true"
const { context, schema } = AppModule;

const printMe = () => {
	console.log("Apollo introspection ... " + APOLLO_INTROSPECTION)
	console.log("Apollo playground ... " + APOLLO_PLAYGROUND)
	console.log("Apollo debug ... " + APOLLO_DEBUG)
	console.log("Schema passed... " + schema)
}

printMe()

const server = new ApolloServer({
	context, 
	debug:APOLLO_DEBUG, 
	introspection:APOLLO_INTROSPECTION, 
	playground:APOLLO_PLAYGROUND, 
	schema:mergeSchemas({
		schemas: [ schema ]
	}), 
	
});

const app = express()

server.applyMiddleware({
	app, path:'/'
})

app.listen({ port: 4000 }, () => {
  console.log('Apollo Server on http://localhost:4000/');
});