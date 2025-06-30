import React, {
    Fragment,
    useMemo,
    useState,
    type ReactElement
} from 'react';
import { useForm } from '../../../../../hooks/useForm';
import { useFocusOnInvalidInput } from '../../../../../hooks/useFocusOnInvalidInput';
import { useChangePassword } from '../../../../../api/authApi';
import { Button } from '../../../../reusable/button/Button';
import { PasswordValidator } from '../../../register/password-validator/PasswordValidator';
import type {
    UserFormData,
    FormSubmissionResult
} from '../../../../../types/User';
import styles from './PasswordUpdateForm.module.scss';
import { InputField } from '../../../../reusable/input-field/InputField';

interface PasswordUpdateFormProps {
    onSuccess: () => void;
}

export const PasswordUpdateForm = ({
    onSuccess
}: PasswordUpdateFormProps): ReactElement => {
    const { changePassword } = useChangePassword();
    const [newPasswordValue, setNewPasswordValue] = useState('');

    const initialFormValues = useMemo<UserFormData>(
        () => ({
            email: { value: '', error: '', valid: false },
            password: { value: '', error: '', valid: false },
            currentPassword: {
                value: '',
                error: '',
                valid: false
            },
            newPassword: { value: '', error: '', valid: false }
        }),
        []
    );

    useFocusOnInvalidInput();

    const handleSubmit = async (
        formData: UserFormData
    ): Promise<FormSubmissionResult> => {
        const currentPassword =
            formData.currentPassword?.value?.trim();
        const newPassword = formData.newPassword?.value?.trim();

        if (!currentPassword || !newPassword) {
            return {
                success: false,
                error: 'Both current and new passwords are required'
            };
        }

        const apiData = {
            current_password: currentPassword,
            new_password: newPassword
        };

        try {
            const result = await changePassword(apiData);

            if (result && !result.error) {
                onSuccess();
                return { success: true };
            }

            return {
                success: false,
                error:
                    result?.error || 'Failed to update password',
                data: result
            };
        } catch {
            return {
                success: false,
                error: 'Failed to update password'
            };
        }
    };

    const formProps = useForm(initialFormValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: false
    });

    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting
    } = formProps;

    const handleNewPasswordChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ) => {
        setNewPasswordValue(e.target.value);
        handleFieldChange(e);
    };

    return (
        <section className={styles['password-update-form']}>
            <h2>Change Password</h2>

            <form action={submitAction}>
                <Fragment>
                    <InputField
                        getInputClassName={getInputClassName}
                        fieldData={formData.currentPassword!}
                        handleFieldChange={handleFieldChange}
                        validateField={validateField}
                        fieldName='currentPassword'
                        type='password'
                    />
                </Fragment>

                <Fragment>
                    <InputField
                        getInputClassName={getInputClassName}
                        fieldData={formData.newPassword!}
                        handleFieldChange={
                            handleNewPasswordChange
                        }
                        validateField={validateField}
                        fieldName='newPassword'
                        type='password'
                    />
                </Fragment>

                <PasswordValidator password={newPasswordValue} />

                <div className={styles['button-group']}>
                    <Button
                        title='Save'
                        color='black'
                        actionType='submit'
                        pending={isSubmitting}
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
