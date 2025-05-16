import { useActionState } from 'react';
import useUserContext from '../../../contexts/UserContext';
import { useRegister } from '../../../api/authApi';
import { AuthLayout } from '../auth-layout/ AuthLayout';
import { useState } from 'react';
import { Button } from '../../reusable/button/Button';
import { useNavigate } from 'react-router';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import { PasswordValidator } from './password-validator/PasswordValidator';

import styles from './Register.module.css';
import { validateFormFields } from '../../../utils/validateFormFields';

export const Register = () => {
    const initialFormValues = {
        email: { value: '', error: '' },
        password: { value: '', error: '' }
    };
    const [isValid, setIsValid] = useState(true);
    const [userData, setUserData] = useState(initialFormValues);

    const { userLoginHandler } = useUserContext();
    const { register } = useRegister();
    const navigate = useNavigate();
    useFocusOnInvalidInput();

    const validateForm = () => {
        let updatedUserData = { ...userData };

        const { validatedUserData, isValid } = validateFormFields(
            userData,
            updatedUserData
        );

        setIsValid(isValid);
        setUserData(validatedUserData);
    };

    const registerHandler = async () => {
        validateForm();

        if (!isValid) {
            return { success: false, error: 'Registration failed' };
        }

        const authData = await register({
            email: userData.email.value,
            password: userData.password.value
        });

        if (authData?.access) {
            userLoginHandler(authData);

            navigate('/my-account/details');
            return { success: true };
        }

        if (authData.email) {
            setUserData((state) => ({
                ...state,
                email: {
                    error: authData.email.join(' '),
                    value: state.email.value
                }
            }));
        }

        if (authData.password) {
            setUserData((state) => ({
                ...state,
                password: {
                    error: authData.password.join(' '),
                    value: state.password.value
                }
            }));
        }

        return { success: false, error: 'Registration failed' };
    };

    const [_, registerAction, isPending] = useActionState(registerHandler, {
        email: userData.email.value,
        password: userData.password.value
    });

    const changeHandler = (e) => {
        const { name, value } = e.target;

        setUserData((state) => ({
            ...state,
            [name]: {
                value,
                error: ''
            }
        }));
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
                            type='text'
                            name='email'
                            id='email'
                            placeholder='email'
                            value={userData.email.value}
                            onChange={changeHandler}
                            onBlur={validateForm}
                        />
                        <label htmlFor='email'>Email</label>
                        {userData.email.error && (
                            <span className={styles['error']}>
                                {userData.email.error}
                            </span>
                        )}
                    </div>

                    <p>Enter your email for important order updates.</p>

                    <div className='field'>
                        <input
                            type='password'
                            name='password'
                            id='password'
                            placeholder='password'
                            value={userData.password.value}
                            onChange={changeHandler}
                            onBlur={validateForm}
                        />
                        <label htmlFor='password'>Password</label>
                        {userData.password.error && (
                            <span className={styles['error']}>
                                {userData.password.error}
                            </span>
                        )}
                    </div>

                    <PasswordValidator
                        password={userData?.password?.value || ''}
                    />

                    <Button
                        title={'Register'}
                        color='black'
                        actionType='submit'
                        pending={isPending}
                    />
                </form>
            </section>
        </AuthLayout>
    );
};
