import 'reflect-metadata';
import resolvers from './resolvers';

describe('Commodities', () => {
	describe('Commodities Name List', () => {
		
		const {
			Query:{ getCommodities:resolver }
		} = resolvers

		test('Sample testing for Commodities names', () => {
			expect(resolver).toBeDefined()
		})
	})
});