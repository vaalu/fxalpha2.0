import config from './env.json'
import keycloak from 'keycloak-js'

export const KEYCLOAK_JSON = keycloak({
	realm:config['realm'], 
	clientId:config['resource'], 
	url:config['auth-server-url']
})
export const APOLLO_SERVER = config['apollo-server']
export const KAFKA_SERVER = config['kafka-server']
export const DATE_CONSTANTS = {
	months : [	"Jan", "Feb", "Mar", "Apr", 
				"May", "Jun", "Jul", "Aug", 
				"Sep", "Oct", "Nov", "Dec" ] 
}