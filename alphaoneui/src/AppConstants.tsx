import keycloak from 'keycloak-js'
import kc from './keycloak.json'

export const KEYCLOAK_JSON = keycloak({
	realm:kc['realm'], 
	clientId:kc['resource'], 
	url:kc['auth-server-url']
})
export const APOLLO_SERVER = 'http://localhost:4000'
export const KAFKA_SERVER = 'localhost:9092'
export const DATE_CONSTANTS = {
	months : [	"Jan", "Feb", "Mar", "Apr", 
				"May", "Jun", "Jul", "Aug", 
				"Sep", "Oct", "Nov", "Dec" ] 
}