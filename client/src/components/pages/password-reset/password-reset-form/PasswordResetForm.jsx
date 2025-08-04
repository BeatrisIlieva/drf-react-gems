import { useState } from 'react';
import { useCallback } from 'react';

import { Button } from '../../../reusable/button/Button';
import { InputField } from '../../../reusable/input-field/InputField';
import { PasswordValidator } from '../../../reusable/password-validator/PasswordValidator';

import { usePasswordResetForm } from '../../../../hooks/usePasswordResetForm';

import styles from './PasswordResetForm.module.scss';

export const PasswordResetForm = ({ uid, token }) => {
    const [passwordsDoNotMatch, setPasswordsDoNotMatch] = useState(false);

    const { formProps, fieldConfig, newPasswordValue, handleNewPasswordChange } =
        usePasswordResetForm({ uid, token });

    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting,
        formRef,
    } = formProps;

    const clickHandler = useCallback(() => {
        if (formData.newPassword.value !== formData.confirmNewPassword.value) {
            setPasswordsDoNotMatch(true);

            return;
        }
        setPasswordsDoNotMatch(false);
        submitAction();
    }, [submitAction, formData]);

    return (
        <section className={styles['password-update-form']}>
            <h2>Reset Password</h2>
            <form ref={formRef} action={clickHandler}>
                <InputField
                    getInputClassName={getInputClassName}
                    fieldData={formData.newPassword}
                    handleFieldChange={handleFieldChange}
                    validateField={validateField}
                    fieldName="newPassword"
                    type="password"
                    fieldConfig={fieldConfig}
                />
                <InputField
                    getInputClassName={getInputClassName}
                    fieldData={formData.confirmNewPassword}
                    handleFieldChange={handleNewPasswordChange}
                    validateField={validateField}
                    fieldName="confirmNewPassword"
                    type="password"
                    fieldConfig={fieldConfig}
                />

                {passwordsDoNotMatch && (
                    <p className={styles['error']}>Passwords don’t match. Please try again.</p>
                )}

                <PasswordValidator password={newPasswordValue} />
                <div className={styles['button-group']}>
                    <Button
                        title="Save"
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
                        callbackHandler={() => {}}
                    />
                </div>
            </form>
        </section>
    );
};
