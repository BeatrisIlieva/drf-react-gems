import useUserContext from '../../../contexts/UserContext';
import { useLogin } from '../../../api/authApi';
import { useActionState } from 'react';
import { useNavigate } from 'react-router';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import { InputField } from '../../reusable/input-field/InputField';
import { Button } from '../../reusable/button/Button';
import { AuthLayout } from '../auth-layout/ AuthLayout';

import { useForm } from '../../../hooks/useForm';

import styles from './Login.module.css'
import { Footer } from './footer/Footer';

export const Login = () => {
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

    const { userLoginHandler } = useUserContext();
    const { login } = useLogin();
    const navigate = useNavigate();

    useFocusOnInvalidInput();

    const loginHandler = async () => {
        const isValid = validateFields();

        if (!isValid) {
            return { success: false, error: 'Login failed' };
        }

        const authData = await login({
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

    const [_, loginAction, isPending] = useActionState(loginHandler, {
        email: userData.email.value,
        password: userData.password.value
    });

    return (
        <AuthLayout>
            <section className={styles['login']}>
            <h2>Welcome Back</h2>
            <p>Please sign in to access your account.</p>
                <form action={loginAction}>
                    {Object.entries(userData).map(([fieldName, fieldData]) => (
                        <InputField
                            key={fieldName}
                            getInputClassName={getInputClassName}
                            fieldData={fieldData}
                            validateField={validateField}
                            fieldName={fieldName}
                            type={
                                fieldName === 'password' ? 'password' : 'text'
                            }
                        />
                    ))}

                    <Button
                        title={'Sign In'}
                        color='black'
                        actionType='submit'
                        pending={isPending}
                    />
                </form>
                <Footer/>
            </section>
        </AuthLayout>
    );
};
