import 'reflect-metadata';
import resolvers from './resolvers';

describe('Alice', () => {
	describe('Alice Blue Connect', () => {
		
		const {
			Query:{ aliceConnect:resolver }
		} = resolvers

		test('Sample testing for alice blue connecion', () => {
			expect(resolver('parent', 'token')).toBeDefined()
		})
	})
});