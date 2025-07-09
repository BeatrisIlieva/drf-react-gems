import {
    Fragment,
    useCallback,
    useState,
    useEffect
} from 'react';
import { useForm } from '../../../../../hooks/useForm';
import { useProfile } from '../../../../../api/useProfileApi';
import { Button } from '../../../../reusable/button/Button';
import { InputField } from '../../../../reusable/input-field/InputField';
import { PasswordValidator } from '../../../../reusable/password-validator/PasswordValidator';
import { FORM_CONFIGS } from '../../../../../config/formFieldConfigs';
import { createApiDataFromForm } from '../../../../../utils/formHelpers';
import styles from './PasswordUpdateForm.module.scss';

export const PasswordUpdateForm = ({ onSuccess }) => {
    const { fieldConfig, initialValues } =
        FORM_CONFIGS.passwordUpdate;
    const { changePassword } = useProfile();
    const [newPasswordValue, setNewPasswordValue] = useState('');

    const handleSubmit = useCallback(
        async (formData) => {
            const apiData = createApiDataFromForm(
                formData,
                fieldConfig
            );

            try {
                const result = await changePassword(apiData);

                if (result && !result.error) {
                    onSuccess();
                    return { success: true };
                }

                if (result && typeof result === 'object') {
                    return {
                        success: false,
                        data: result
                    };
                }

                return {
                    success: false,
                    error: 'Failed to update password'
                };
            } catch {
                return {
                    success: false,
                    error: 'Failed to update password'
                };
            }
        },
        [fieldConfig, changePassword, onSuccess]
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
        isSubmitting,
        resetValidationStates,
        formRef,
        registerInput
    } = formProps;

    const handleNewPasswordChange = (e) => {
        setNewPasswordValue(e.target.value);
        handleFieldChange(e);
    };

    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    return (
        <section className={styles['password-update-form']}>
            <h2>Change Password</h2>

            <form ref={formRef} action={submitAction}>
                <Fragment>
                    <InputField
                        getInputClassName={getInputClassName}
                        fieldData={formData.currentPassword}
                        handleFieldChange={handleFieldChange}
                        validateField={validateField}
                        fieldName='currentPassword'
                        type='password'
                        registerInput={registerInput}
                        fieldConfig={fieldConfig}
                    />
                </Fragment>

                <Fragment>
                    <InputField
                        getInputClassName={getInputClassName}
                        fieldData={formData.newPassword}
                        handleFieldChange={
                            handleNewPasswordChange
                        }
                        validateField={validateField}
                        fieldName='newPassword'
                        type='password'
                        registerInput={registerInput}
                        fieldConfig={fieldConfig}
                    />
                </Fragment>

                <PasswordValidator password={newPasswordValue} />

                <div className={styles['button-group']}>
                    <Button
                        title='Save'
                        color='black'
                        actionType='submit'
                        pending={isSubmitting}
                        success={formProps.formState?.success}
                        callbackHandler={() => {}}
                    />
                    <Button
                        title='Cancel'
                        color='white'
                        actionType='button'
                        callbackHandler={onSuccess}
                    />
                </div>
            </form>
        </section>
    );
};
