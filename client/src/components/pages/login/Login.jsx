import { Fragment, useState } from 'react';
import { useNavigate } from 'react-router';
import { useForm } from '../../../hooks/useForm';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import { useUserContext } from '../../../contexts/UserContext';
import { useLogin } from '../../../api/authApi';
import { InputField } from '../../reusable/input-field/InputField';
import { Button } from '../../reusable/button/Button';
import { AuthLayout } from '../../reusable/auth-layout/AuthLayout';

import styles from './Login.module.scss';

import { Footer } from './footer/Footer';

export const Login = () => {
    const initialFormValues = {
        email_or_username: { value: '', error: '', valid: false },
        password: { value: '', error: '', valid: false }
    };

    const { userLoginHandler } = useUserContext();
    const { login } = useLogin();
    const navigate = useNavigate();

    useFocusOnInvalidInput();

    const [
        invalidUsernameOrPassword,
        setInvalidUsernameOrPassword
    ] = useState(false);

    const handleSubmit = async (formData) => {
        setInvalidUsernameOrPassword(false);

        const authData = await login({
            email_or_username: formData.email_or_username.value,
            password: formData.password.value
        });

        if (authData?.access) {
            userLoginHandler(authData);
            navigate('/my-account/details');
            return { success: true };
        }

        if (
            authData === undefined ||
            authData === 'Invalid username or password'
        ) {
            setInvalidUsernameOrPassword(true);
            return {
                success: false,
                error: 'Invalid username or password'
            };
        }

        // Handle server-side field-specific errors
        if (authData && typeof authData === 'object' && !authData.access) {
            const hasFieldErrors = handleServerSideErrors(authData);
            
            // If no field-specific errors, show general error
            if (!hasFieldErrors) {
                setInvalidUsernameOrPassword(true);
            }
            
            return {
                success: false,
                error: 'Login failed'
            };
        }

        return { success: false, error: 'Login failed' };
    };

    const formProps = useForm(initialFormValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true
    });

    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting,
        handleServerSideErrors
    } = formProps;

    return (
        <AuthLayout>
            <section className={styles['login']}>
                <h2>Welcome Back</h2>
                <p>Please sign in to access your account.</p>
                {invalidUsernameOrPassword && (
                    <div
                        className={
                            styles['invalid-username-password']
                        }
                    >
                        <p>
                            Your email/username or password is
                            incorrect. Try again or reset your
                            password.
                        </p>
                    </div>
                )}

                <form action={submitAction}>
                    {Object.entries(formData).map(
                        ([fieldName, fieldData]) => (
                            <Fragment key={fieldName}>
                                {fieldData && (
                                    <InputField
                                        getInputClassName={
                                            getInputClassName
                                        }
                                        fieldData={fieldData}
                                        handleFieldChange={
                                            handleFieldChange
                                        }
                                        validateField={
                                            validateField
                                        }
                                        fieldName={fieldName}
                                        type={
                                            fieldName ===
                                            'password'
                                                ? 'password'
                                                : 'text'
                                        }
                                    />
                                )}
                            </Fragment>
                        )
                    )}

                    <Button
                        title={'Sign In'}
                        color='black'
                        actionType='submit'
                        pending={isSubmitting}
                        callbackHandler={() => {}}
                    />
                </form>
                <Footer />
            </section>
        </AuthLayout>
    );
};
