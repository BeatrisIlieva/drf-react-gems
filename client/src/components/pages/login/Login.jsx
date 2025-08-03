import { useState } from 'react';

import { AuthLayout } from '../../reusable/auth-layout/AuthLayout';
import { Button } from '../../reusable/button/Button';
import { InputField } from '../../reusable/input-field/InputField';
import { Popup } from '../../reusable/popup/Popup';
import { ErrorMessage } from './error-message/ErrorMessage';
import { Footer } from './footer/Footer';
import { ResetPasswordRequest } from './reset-password-request/ResetPasswordRequest';

import { useForm } from '../../../hooks/useForm';
import { useLogin } from '../../../hooks/useLogin';

import { FORM_CONFIGS } from '../../../config/formFieldConfigs';

import styles from './Login.module.scss';

export const Login = () => {
    const { fieldConfig, initialValues } = FORM_CONFIGS.login;
    const { handleSubmit, invalidCredentials } = useLogin(fieldConfig);
    const [isPopupOpen, setIsPopupOpen] = useState(false);

    const formProps = useForm(initialValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true,
    });

    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting,
    } = formProps;

    return (
        <AuthLayout>
            <section className={styles['login']}>
                <h2>Welcome Back</h2>
                <p>Please sign in to access your account.</p>

                <ErrorMessage show={invalidCredentials} />

                <form action={submitAction}>
                    {Object.entries(formData).map(
                        ([fieldName, fieldData]) =>
                            fieldData && (
                                <InputField
                                    key={fieldName}
                                    getInputClassName={getInputClassName}
                                    fieldData={fieldData}
                                    handleFieldChange={handleFieldChange}
                                    validateField={validateField}
                                    fieldName={fieldName}
                                    fieldConfig={fieldConfig}
                                />
                            )
                    )}

                    <button
                        type="button"
                        className={styles['forgot-password']}
                        onClick={() => setIsPopupOpen(true)}
                    >
                        Forgot your password?
                    </button>

                    <Button
                        title="Sign In"
                        color="black"
                        actionType="submit"
                        pending={isSubmitting}
                        success={formProps.formState?.success}
                        callbackHandler={() => {}}
                    />
                </form>

                <Footer />
            </section>

            {isPopupOpen && (
                <Popup isOpen={isPopupOpen} onClose={() => setIsPopupOpen(false)}>
                    <ResetPasswordRequest onClose={() => setIsPopupOpen(false)} />
                </Popup>
            )}
        </AuthLayout>
    );
};
