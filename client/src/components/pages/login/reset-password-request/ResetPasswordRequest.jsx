import { useState } from 'react';

import { Button } from '../../../reusable/button/Button';
import { InputField } from '../../../reusable/input-field/InputField';

import { useAuthentication } from '../../../../api/authApi';

import { useForm } from '../../../../hooks/useForm';

import { FORM_CONFIGS } from '../../../../config/formFieldConfigs';

import styles from './ResetPasswordRequest.module.scss';

export const ResetPasswordRequest = ({ onClose }) => {
    const { resetPasswordRequest } = useAuthentication();
    const [isSubmitted, setIsSubmitted] = useState(false);

    const { fieldConfig, initialValues } = FORM_CONFIGS.emailFieldForResetPassword;

    const formProps = useForm(initialValues, {
        onSubmit: resetPasswordRequest,
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

    const clickHandler = () => {
        submitAction();
        setIsSubmitted(true);
    };

    return (
        <section className={styles['reset-password-request']}>
            <h3>{!isSubmitted ? 'Forgot your password?' : 'Request received'}</h3>
            <p>
                {!isSubmitted
                    ? 'Enter your email to receive password reset instructions.'
                    : 'If an email address matching that account exists, we have sent a password reset link to it.'}
            </p>

            {!isSubmitted && (
                <form action={clickHandler}>
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
                    <Button
                        title="Send"
                        color="black"
                        actionType="submit"
                        pending={isSubmitting}
                        success={formProps.formState?.success}
                        callbackHandler={() => {}}
                    />

                    <Button
                        title="Cancel"
                        color="white"
                        actionType="button"
                        callbackHandler={() => onClose()}
                    />
                </form>
            )}
        </section>
    );
};
