import { useActionState } from 'react';
import useUserContext from '../../../contexts/UserContext';
import { useRegister } from '../../../api/authApi';
import { AuthLayout } from '../auth-layout/ AuthLayout';
import { useEffect } from 'react';
import { Button } from '../../reusable/button/Button';
import { useNavigate } from 'react-router';
import {useFocusOnInvalidInput} from '../../../hooks/useFocusOnInvalidInput'

import styles from './Register.module.css';

export const Register = () => {
    const { userLoginHandler } = useUserContext();
    const { register } = useRegister();
    const navigate = useNavigate();
    useFocusOnInvalidInput()

    const registerHandler = async (_, formData) => {
        const email = formData.get('email');
        const password = formData.get('password');

        const authData = await register({ email, password });

        if (authData?.access) {
            userLoginHandler(authData);

            navigate('/my-account/details');
            return { success: true };
        }

        return { success: false, error: 'Registration failed' };
    };

    const [state, registerAction, isPending] = useActionState(registerHandler, {
        email: '',
        password: ''
    });

    // useEffect(() => {
    //     const handleInvalid = (e) => {
    //         e.preventDefault();

    //         // Use :invalid to find first invalid input
    //         const invalidElements = document.querySelectorAll('input:invalid');

    //         if (invalidElements.length > 0) {
    //             const firstInvalid = invalidElements[0];
    //             firstInvalid.focus();
    //         }
    //     };

    //     // Use capture phase to catch invalid events before browser handles them
    //     document.addEventListener('invalid', handleInvalid, true);

    //     return () => {
    //         document.removeEventListener('invalid', handleInvalid, true);
    //     };
    // }, []);

    // const navigateHandler = () => {
    //     navigate('/my-account/details');
    // };

    return (
        <AuthLayout>
            <section className={styles['register']}>
                <p>Back to Sign In</p>
                <h2>Create Account</h2>
                <form action={registerAction}>
                    <div className='field'>
                        <input
                            type='email'
                            name='email'
                            id='email'
                            placeholder='email'
                            required
                        />
                        <label htmlFor='email'>Email</label>
                    </div>

                    <p>Enter your email for important order updates.</p>

                    <div className='field'>
                        <input
                            type='password'
                            name='password'
                            id='password'
                            placeholder='password'
                            required
                        />
                        <label htmlFor='password'>Password</label>
                    </div>
                    <Button
                        title={'Register'}
                        color='black'
                        actionType='submit'
                        pending={isPending}
                    />

                    {state.error && (
                        <p style={{ color: 'red' }}>{state.error}</p>
                    )}
                </form>
            </section>
        </AuthLayout>
    );
};
