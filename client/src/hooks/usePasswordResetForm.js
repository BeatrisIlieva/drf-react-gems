import { useCallback, useEffect, useState } from 'react';

import { useNavigate } from 'react-router';

import { useForm } from './useForm';

import { useAuthentication } from '../api/authApi';

import { createApiDataFromForm } from '../utils/formHelpers';

import { FORM_CONFIGS } from '../config/formFieldConfigs';

export const usePasswordResetForm = ({ uid, token }) => {
    const { resetPasswordConfirm } = useAuthentication();

    const [newPasswordValue, setNewPasswordValue] = useState('');

    const { fieldConfig, initialValues } = FORM_CONFIGS.passwordReset;

    const navigate = useNavigate();

    const handleSubmit = useCallback(
        async formData => {
            const apiData = createApiDataFromForm(formData, fieldConfig);

            try {
                const result = await resetPasswordConfirm(apiData, uid, token);

                if (result && !result.error) {
                    navigate('/my-account/login');
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
        [fieldConfig, resetPasswordConfirm]
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
