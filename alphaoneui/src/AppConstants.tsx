import keycloak from 'keycloak-js'

export const KEYCLOAK_JSON = keycloak({
	realm:'AlphaPrime', 
	clientId:'alphaprimeui', 
	url:'http://localhost:8080/auth' 
})
export const APOLLO_SERVER = 'http://localhost:4000'
export const KAFKA_SERVER = 'localhost:9092'
export const DATE_CONSTANTS = {
	months : [	"Jan", "Feb", "Mar", "Apr", 
				"May", "Jun", "Jul", "Aug", 
				"Sep", "Oct", "Nov", "Dec" ] 
}