import React, { Fragment, useState } from 'react';
import { useNavigate } from 'react-router';
import useUserContext from '../../../contexts/UserContext';
import { useLogin, useRegister } from '../../../api/authApi';
import { AuthLayout } from '../../reusable/auth-layout/AuthLayout';
import { InputField } from '../../reusable/input-field/InputField';
import { Button } from '../../reusable/button/Button';
import { PasswordValidator } from './password-validator/PasswordValidator';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import { useRegisterForm } from '../../../hooks/useRegisterForm';
import type { RegisterFormData } from '../../../types/User';

import styles from './Register.module.scss';
import { Icon } from '../../reusable/icon/Icon';

// Since useActionState is React 19+ feature, we'll create a simple alternative
interface ActionState<T> {
    status: 'idle' | 'pending' | 'success' | 'error';
    data?: T;
    error?: Error;
}

type ActionFunction<T> = () => Promise<T>;

// Simple useActionState alternative
function useActionState<T>(
    action: ActionFunction<T>
): [ActionState<T>, () => Promise<T>, boolean] {
    const [state, setState] = useState<ActionState<T>>({
        status: 'idle'
    });

    const actionFn = async () => {
        setState({ status: 'pending' });
        try {
            const result = await action();
            setState({ status: 'success', data: result });
            return result;
        } catch (error) {
            const err =
                error instanceof Error
                    ? error
                    : new Error(String(error));
            setState({ status: 'error', error: err });
            throw err;
        }
    };

    const isPending = state.status === 'pending';

    return [state, actionFn, isPending];
}

export const Register: React.FC = () => {
    const initialFormValues: RegisterFormData = {
        email: { value: '', error: '', valid: false },
        username: { value: '', error: '', valid: false },
        password: { value: '', error: '', valid: false }
    };

    const {
        registerData,
        validateFields,
        validateField,
        handleFieldChange,
        setServerSideError,
        getInputClassName
    } = useRegisterForm(initialFormValues);

    const [agree, setAgree] = useState<boolean>(true);

    const { userLoginHandler } = useUserContext();
    const { register } = useRegister();
    const { login } = useLogin();
    const navigate = useNavigate();

    useFocusOnInvalidInput();

    const registerHandler = async () => {
        const isValid = validateFields();

        if (!isValid) {
            return {
                success: false,
                error: 'Registration failed'
            };
        }

        const authData = await register({
            email: registerData.email.value,
            username: registerData.username.value,
            password: registerData.password.value
        });

        if (authData?.access) {
            userLoginHandler(authData);

            await login({
                email_or_username: registerData.email.value,
                password: registerData.password.value
            });

            navigate('/my-account/details');
            return { success: true };
        }

        Object.keys(initialFormValues).forEach((key) => {
            if (authData && typeof authData === 'object') {
                setServerSideError(
                    authData as unknown as Record<string, string[]>,
                    key
                );
            }
        });

        return { success: false };
    };

    const [, registerAction, isPending] =
        useActionState(registerHandler);

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

                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        registerAction();
                    }}
                >
                    {Object.entries(registerData).map(
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
                                            Choose a unique username 
                                            for your account.
                                        </p>
                                    )}
                            </Fragment>
                        )
                    )}

                    <PasswordValidator
                        password={registerData?.password?.value || ''}
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
                        pending={isPending}
                        callbackHandler={() => {}}
                    />
                </form>
            </section>
        </AuthLayout>
    );
};
