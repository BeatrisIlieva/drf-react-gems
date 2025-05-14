import { useActionState } from 'react';
import useUserContext from '../../../contexts/UserContext';
import { useRegister } from '../../../api/authApi';

export const Register = () => {
    const { userLoginHandler } = useUserContext();
    const { register } = useRegister();

    const registerHandler = async (_, formData) => {
        const email = formData.get('email');
        const password = formData.get('password');

        const authData = await register({ email, password });

        if (authData?.access) {
            userLoginHandler(authData);
            return { success: true };
        }

        return { success: false, error: 'Registration failed' };
    };

    const [state, registerAction, isPending] = useActionState(registerHandler, {
        email: '',
        password: ''
    });

    return (
        <form action={registerAction}>
            <input type='email' name='email' placeholder='email' required />
            <input
                type='password'
                name='password'
                placeholder='password'
                required
            />
            <input
                type='submit'
                value={isPending ? 'Registering...' : 'Register'}
            />
            {state.error && <p style={{ color: 'red' }}>{state.error}</p>}
        </form>
    );
};
