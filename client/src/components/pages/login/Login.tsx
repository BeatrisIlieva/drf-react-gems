import React, { Fragment, useState } from 'react';
import { useNavigate } from 'react-router';
import { useLoginForm } from '../../../hooks/useLoginForm';
import { useFocusOnInvalidInput } from '../../../hooks/useFocusOnInvalidInput';
import useUserContext from '../../../contexts/UserContext';
import { useLogin } from '../../../api/authApi';
import { InputField } from '../../reusable/input-field/InputField';
import { Button } from '../../reusable/button/Button';
import { AuthLayout } from '../../reusable/auth-layout/AuthLayout';

import styles from './Login.module.scss';
import type { LoginFormData } from '../../../types/User';
import { Footer } from './footer/Footer';

// Since useActionState is React 19+ feature, we'll use our own implementation
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

export const Login: React.FC = () => {
    const initialFormValues: LoginFormData = {
        email_or_username: { value: '', error: '', valid: false },
        password: { value: '', error: '', valid: false }
    };

    const {
        loginData,
        validateFields,
        validateField,
        handleFieldChange,
        setServerSideError,
        getInputClassName
    } = useLoginForm(initialFormValues);

    const { userLoginHandler } = useUserContext();
    const { login } = useLogin();
    const navigate = useNavigate();

    useFocusOnInvalidInput();

    const [
        invalidUsernameOrPassword,
        setInvalidUsernameOrPassword
    ] = useState(false);

    const loginHandler = async () => {
        const isValid = validateFields();

        if (!isValid) {
            return { success: false, error: 'Login failed' };
        }

        const authData = await login({
            email_or_username: loginData.email_or_username.value,
            password: loginData.password.value
        });

        if (authData?.access) {
            userLoginHandler(authData);

            navigate('/my-account/details');
            return { success: true };
        }

        if (
            authData === undefined ||
            (authData as string) ===
                'Invalid username or password'
        ) {
            setInvalidUsernameOrPassword(true);
        }

        // Handle server-side errors
        Object.keys(initialFormValues).forEach((key) => {
            if (authData && typeof authData === 'object') {
                setServerSideError(
                    authData as Record<string, string[]>,
                    key
                );
            }
        });

        return { success: false };
    };

    const [, loginAction, isPending] =
        useActionState(loginHandler);

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
                            Your email/username or password is incorrect.
                            Try again or reset your password.
                        </p>
                    </div>
                )}

                <form
                    onSubmit={(e) => {
                        e.preventDefault();
                        loginAction();
                    }}
                >
                    {Object.entries(loginData).map(
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
                        pending={isPending}
                        callbackHandler={() => {}}
                    />
                </form>
                <Footer />
            </section>
        </AuthLayout>
    );
};
