import 'reflect-metadata';
import resolvers from './resolvers';

describe('Nifty50', () => {
	describe('Nifty50 Name List', () => {
		
		const {
			Query:{ getNifty50:resolver }
		} = resolvers

		test('Sample testing for Nifty 50 equities names', () => {
			expect(resolver).toBeDefined()
		})
	})
});