import { Button } from '../../../../../reusable/button/Button';
import { InputField } from '../../../../../reusable/input-field/InputField';
import { PasswordValidator } from '../../../../../reusable/password-validator/PasswordValidator';

import { usePasswordUpdateForm } from '../../../../../../hooks/usePasswordUpdateForm';

import styles from './PasswordUpdateForm.module.scss';

export const PasswordUpdateForm = ({ onSuccess = null }) => {
    const { formProps, fieldConfig, newPasswordValue, handleNewPasswordChange } =
        usePasswordUpdateForm(onSuccess);
    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting,
        formRef,
    } = formProps;
    return (
        <section className={styles['password-update-form']}>
            <h2>Change Password</h2>
            <form ref={formRef} action={submitAction}>
                <InputField
                    getInputClassName={getInputClassName}
                    fieldData={formData.currentPassword}
                    handleFieldChange={handleFieldChange}
                    validateField={validateField}
                    fieldName="currentPassword"
                    type="password"
                    fieldConfig={fieldConfig}
                />
                <InputField
                    getInputClassName={getInputClassName}
                    fieldData={formData.newPassword}
                    handleFieldChange={handleNewPasswordChange}
                    validateField={validateField}
                    fieldName="newPassword"
                    type="password"
                    fieldConfig={fieldConfig}
                />
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
                        callbackHandler={onSuccess}
                    />
                </div>
            </form>
        </section>
    );
};
