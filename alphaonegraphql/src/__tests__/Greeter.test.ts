import { Greeter } from '../components/Greeter';

test ('Greeter Test', () => {
	expect(Greeter('Jeani')).toBe('Hello Jeani');
});