import { useActionState } from 'react';
import useUserContext from '../../../contexts/UserContext';
import { useLogin, useRegister } from '../../../api/authApi';
import { AuthLayout } from '../auth-layout/ AuthLayout';
import { useState } from 'react';
import { Button } from '../../reusable/button/Button';
import { useNavigate } from 'react-router';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import { PasswordValidator } from './password-validator/PasswordValidator';
import { useForm } from '../../../hooks/useForm';
import styles from './Register.module.css';
import { InputField } from '../../reusable/input-field/InputField';
import { Fragment } from 'react';

export const Register = () => {
    const initialFormValues = {
        email: { value: '', error: '', valid: false },
        password: { value: '', error: '', valid: false }
    };

    const {
        userData,
        validateFields,
        validateField,
        setServerSideError,
        getInputClassName
    } = useForm(initialFormValues);

    const [agree, setAgree] = useState(true);

    const { userLoginHandler } = useUserContext();
    const { register } = useRegister();
    const { login } = useLogin()
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

            await login({
                email: userData.email.value,
                password: userData.password.value
            });

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

    const navigateToLoginHandler = () => {
        navigate('/my-account/login');
    };

    return (
        <AuthLayout>
            <section className={styles['register']}>
                <p onClick={navigateToLoginHandler}>
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
                    {Object.entries(userData).map(([fieldName, fieldData]) => (
                        <Fragment key={fieldName}>
                            <InputField
                                getInputClassName={getInputClassName}
                                fieldData={fieldData}
                                validateField={validateField}
                                fieldName={fieldName}
                                type={
                                    fieldName === 'password'
                                        ? 'password'
                                        : 'text'
                                }
                            />
                            {fieldName === 'email' && (
                                <p>
                                    Enter your email for important order
                                    updates.
                                </p>
                            )}
                        </Fragment>
                    ))}

                    <PasswordValidator
                        password={userData?.password?.value || ''}
                    />

                    <div className={styles['terms-wrapper']}>
                        <input
                            type='checkbox'
                            name='agree'
                            id='agree'
                            checked={agree}
                            onChange={() => setAgree(!agree)}
                        />
                        <label className={styles['agree']}>
                            By creating an account, you agree to receive email
                            updates*
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
