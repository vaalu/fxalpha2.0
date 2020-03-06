import { AliceConnect } from '../../datasources'

export default {

	Query: {
		aliceConnect : (parent:any, args:any) => {
			console.log('Token passed: ', args.token)
			const alice = new AliceConnect()
			const connectResponse = alice.connect(args.token)
			return connectResponse
		}, 
		aliceProfile : async () => {
			const profile = new AliceConnect()
			const profileResponse = profile.getProfile()
			return profileResponse
		}
	}
}