import { useActionState } from 'react';
import useUserContext from '../../../contexts/UserContext';
import { useRegister } from '../../../api/authApi';
import { AuthLayout } from '../auth-layout/ AuthLayout';
import { useEffect, useState } from 'react';
import { Button } from '../../reusable/button/Button';
import { useNavigate } from 'react-router';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import { PasswordValidator } from './password-validator/PasswordValidator';

import styles from './Register.module.css';

export const Register = () => {
    const { userLoginHandler } = useUserContext();
    const { register } = useRegister();
    const navigate = useNavigate();
    useFocusOnInvalidInput();
    const [password, setPassword] = useState('');

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

    const passwordChangeHandler = (e) => {
        setPassword(e.target.value);
        console.log(password);
    };
    return (
        <AuthLayout>
            <section className={styles['register']}>
                <p>
                    <svg
                        xmlns='http://www.w3.org/2000/svg'
                        fill='none'
                        viewBox='0 0 24 24'
                        strokeWidth={1.5}
                        stroke='currentColor'
                    >
                        <path
                            strokeLinecap='round'
                            strokeLinejoin='round'
                            d='M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18'
                        />
                    </svg>

                    <span>Back to Sign In</span>
                </p>

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
                            onChange={passwordChangeHandler}
                        />
                        <label htmlFor='password'>Password</label>
                    </div>

                    <PasswordValidator password={password} />

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
