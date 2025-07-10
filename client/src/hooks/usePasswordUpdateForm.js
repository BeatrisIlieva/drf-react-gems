import { useCallback, useEffect, useState } from 'react';

import { useForm } from './useForm';

import { useProfile } from '../api/useProfileApi';

import { createApiDataFromForm } from '../utils/formHelpers';

import { FORM_CONFIGS } from '../config/formFieldConfigs';

export const usePasswordUpdateForm = onSuccess => {
    const { changePassword } = useProfile();

    const [newPasswordValue, setNewPasswordValue] = useState('');

    const { fieldConfig, initialValues } = FORM_CONFIGS.passwordUpdate;

    const handleSubmit = useCallback(
        async formData => {
            const apiData = createApiDataFromForm(formData, fieldConfig);

            try {
                const result = await changePassword(apiData);

                if (result && !result.error) {
                    onSuccess();
                    return { success: true };
                }

                if (result && typeof result === 'object') {
                    return {
                        success: false,
                        data: result,
                    };
                }

                return {
                    success: false,
                    error: 'Failed to update password',
                };
            } catch {
                return {
                    success: false,
                    error: 'Failed to update password',
                };
            }
        },
        [fieldConfig, changePassword, onSuccess]
    );

    const formProps = useForm(initialValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true,
    });

    const { handleFieldChange, resetValidationStates } = formProps;

    const handleNewPasswordChange = e => {
        setNewPasswordValue(e.target.value);
        handleFieldChange(e);
    };

    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    return {
        formProps,
        fieldConfig,
        newPasswordValue,
        handleNewPasswordChange,
    };
};
