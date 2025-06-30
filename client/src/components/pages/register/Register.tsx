import React, { Fragment, useState, useMemo } from 'react';
import { useNavigate } from 'react-router';
import useUserContext from '../../../contexts/UserContext';
import { useLogin, useRegister } from '../../../api/authApi';
import { AuthLayout } from '../../reusable/auth-layout/AuthLayout';
import { InputField } from '../../reusable/input-field/InputField';
import { Button } from '../../reusable/button/Button';
import { PasswordValidator } from './password-validator/PasswordValidator';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import { useForm } from '../../../hooks/useForm';
import type {
    RegisterFormData,
    FormSubmissionResult
} from '../../../types/User';

import styles from './Register.module.scss';
import { Icon } from '../../reusable/icon/Icon';

export const Register: React.FC = () => {
    const initialFormValues = useMemo<RegisterFormData>(
        () => ({
            email: { value: '', error: '', valid: false },
            username: { value: '', error: '', valid: false },
            password: { value: '', error: '', valid: false }
        }),
        []
    );

    const [agree, setAgree] = useState<boolean>(true);

    const { userLoginHandler } = useUserContext();
    const { register } = useRegister();
    const { login } = useLogin();
    const navigate = useNavigate();

    useFocusOnInvalidInput();

    const handleSubmit = async (
        formData: RegisterFormData
    ): Promise<FormSubmissionResult> => {
        const authData = await register({
            email: formData.email.value,
            username: formData.username.value,
            password: formData.password.value
        });

        if (authData?.access) {
            userLoginHandler(authData);

            await login({
                email_or_username: formData.email.value,
                password: formData.password.value
            });

            navigate('/my-account/details');
            return { success: true };
        }

        if (
            authData &&
            typeof authData === 'object' &&
            !authData.access
        ) {
            const serverData = authData as unknown as Record<
                string,
                string[]
            >;
            Object.keys(initialFormValues).forEach((key) => {
                if (serverData[key]) {
                    setServerSideError(serverData, key);
                }
            });

            return {
                success: false,
                error: 'Registration failed',
                data: authData as unknown as Record<
                    string,
                    string[]
                >
            };
        }

        return { success: false, error: 'Registration failed' };
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
        setServerSideError
    } = formProps;

    const navigateToLoginHandler = () => {
        navigate('/my-account/login');
    };

    return (
        <AuthLayout>
            <section className={styles['register']}>
                <p onClick={navigateToLoginHandler}>
                    <Icon name='arrowLeft' />

                    <span>Back to Sign In</span>
                </p>

                <h2>Create Account</h2>

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
                                {fieldName === 'email' &&
                                    fieldData && (
                                        <p>
                                            Enter your email for
                                            important order
                                            updates.
                                        </p>
                                    )}
                                {fieldName === 'username' &&
                                    fieldData && (
                                        <p>
                                            Choose a unique
                                            username for your
                                            account.
                                        </p>
                                    )}
                            </Fragment>
                        )
                    )}

                    <PasswordValidator
                        password={formData?.password?.value || ''}
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
                            By creating an account, you agree to
                            receive email updates*
                        </label>
                    </div>

                    <Button
                        title={'Register'}
                        color='black'
                        actionType='submit'
                        pending={isSubmitting}
                        callbackHandler={() => {}}
                    />
                </form>
            </section>
        </AuthLayout>
    );
};
