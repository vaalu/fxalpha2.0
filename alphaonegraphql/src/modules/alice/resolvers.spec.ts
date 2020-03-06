import 'reflect-metadata';
import resolvers from './resolvers';

describe('Alice', () => {
	describe('Alice Blue Connect', () => {
		
		const {
			Query:{ aliceAntCommodityScrips:resolver }
		} = resolvers

		test('Sample testing for alice blue connecion', () => {
			expect(resolver().then((val) => {
				expect(val).toBe({})
			}))
		})
	})
});