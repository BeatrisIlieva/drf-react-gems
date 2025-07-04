import { Fragment, useState, useCallback } from 'react';
import { useNavigate } from 'react-router';
import { useForm } from '../../../hooks/useForm';
import { useUserContext } from '../../../contexts/UserContext';
import { useAuthentication } from '../../../api/accounts/authApi';
import { InputField } from '../../reusable/input-field/InputField';
import { Button } from '../../reusable/button/Button';
import { AuthLayout } from '../../reusable/auth-layout/AuthLayout';
import { FORM_CONFIGS } from '../../../config/formFieldConfigs';
import { createApiDataFromForm } from '../../../utils/formHelpers';

import styles from './Login.module.scss';

import { Footer } from './footer/Footer';

export const Login = () => {
    const { fieldConfig, initialValues } = FORM_CONFIGS.login;
    const { userLoginHandler } = useUserContext();
    const { login } = useAuthentication();
    const navigate = useNavigate();

    const [invalidCredentials, setInvalidCredentials] =
        useState(false);

    const handleSubmit = useCallback(
        async (formData) => {
            setInvalidCredentials(false);

            const apiData = createApiDataFromForm(
                formData,
                fieldConfig
            );

            const authData = await login(apiData);

            if (authData?.access) {
                userLoginHandler(authData);
                navigate('/my-account/details');
                return { success: true };
            }

            if (
                authData === undefined ||
                authData === 'Invalid username or password'
            ) {
                setInvalidCredentials(true);
                return {
                    success: false,
                    error: 'Invalid username or password'
                };
            }

            if (
                authData &&
                typeof authData === 'object' &&
                !authData.access
            ) {
                return {
                    success: false,
                    data: authData
                };
            }

            return { success: false, error: 'Login failed' };
        },
        [fieldConfig, login, userLoginHandler, navigate]
    );

    const formProps = useForm(initialValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true
    });

    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting
    } = formProps;

    return (
        <AuthLayout>
            <section className={styles['login']}>
                <h2>Welcome Back</h2>
                <p>Please sign in to access your account.</p>
                {invalidCredentials && (
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
                                        fieldConfig={fieldConfig}
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
                        success={formProps.formState?.success}
                        callbackHandler={() => {}}
                    />
                </form>
                <Footer />
            </section>
        </AuthLayout>
    );
};
