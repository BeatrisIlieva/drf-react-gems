import { useActionState } from 'react';
import useUserContext from '../../../contexts/UserContext';
import { useRegister } from '../../../api/authApi';
import { AuthLayout } from '../auth-layout/ AuthLayout';
import { useState } from 'react';
import { Button } from '../../reusable/button/Button';
import { useNavigate } from 'react-router';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import { PasswordValidator } from './password-validator/PasswordValidator';
import { useForm } from '../../../hooks/useForm';
import styles from './Register.module.css';

export const Register = () => {
    const initialFormValues = {
        email: { value: '', error: '' },
        password: { value: '', error: '' }
    };

    const {
        userData,
        validateFields,
        validateField,
        changeHandler,
        setServerSideError
    } = useForm(initialFormValues);

    const [agree, setAgree] = useState(true);

    const { userLoginHandler } = useUserContext();
    const { register } = useRegister();
    const navigate = useNavigate();

    useFocusOnInvalidInput();

    const registerHandler = async () => {
        const isValid = validateFields();

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

        Object.keys(initialFormValues).forEach((key) => {
            setServerSideError(authData, key);
        });
    };

    const [_, registerAction, isPending] = useActionState(registerHandler, {
        email: userData.email.value,
        password: userData.password.value
    });

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
                            className={`${
                                userData.email.error ? 'invalid' : ''
                            }`.trim()}
                            type='text'
                            name='email'
                            id='email'
                            required
                            placeholder='email'
                            value={userData.email.value}
                            onChange={changeHandler}
                            onBlur={validateField}
                        />
                        <label
                            htmlFor='email'
                            className={`${
                                userData.email.error ? 'invalid' : ''
                            }`.trim()}
                        >
                            Email
                        </label>
                        {userData.email.error && (
                            <span className='error'>
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
                            required
                            placeholder='password'
                            value={userData.password.value}
                            onChange={changeHandler}
                            onBlur={validateField}
                            className={`${
                                userData.password.error ? 'invalid' : ''
                            }`.trim()}
                        />
                        <label
                            htmlFor='password'
                            className={`${
                                userData.password.error ? 'invalid' : ''
                            }`.trim()}
                        >
                            Password
                        </label>
                        {userData.password.error && (
                            <span className='error'>
                                {userData.password.error}
                            </span>
                        )}
                    </div>

                    <PasswordValidator
                        password={userData?.password?.value || ''}
                    />

                    <div className={styles['terms-wrapper']}>
                        <input
                            type='checkbox'
                            name='agree'
                            id='agree'
                            required
                            checked={agree}
                            onChange={() => setAgree(!agree)}
                        />
                        <label className={styles['agree']}>
                            By creating an account, you agree to receive email
                            updates
                        </label>
                    </div>

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
