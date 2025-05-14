import useUserContext from '../../../contexts/UserContext';
import { useLogin } from '../../../api/authApi';
import { useActionState } from 'react';

export const Login = () => {
    const { userLoginHandler } = useUserContext();
    const { login } = useLogin();

    const registerHandler = async (_, formData) => {
        const email = formData.get('email');
        const password = formData.get('password');

        const authData = await login({ username: email, password });

        if (authData?.access) {
            userLoginHandler(authData);
            return { success: true };
        }

        return { success: false, error: 'Login failed' };
    };

    const [state, loginAction, isPending] = useActionState(registerHandler, {
        email: '',
        password: ''
    });


    return (
        <form action={loginAction}>
            <input type='email' name='email' placeholder='email' required />
            <input
                type='password'
                name='password'
                placeholder='password'
                required
            />
            <input
                type='submit'
                value={isPending ? 'Login...' : 'Login'}
            />
            {state.error && <p style={{ color: 'red' }}>{state.error}</p>}
        </form>
    );
};
