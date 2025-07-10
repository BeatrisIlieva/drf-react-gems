import { useCallback, useEffect } from 'react';

import { useForm } from './useForm';
import { useFormDataLoader } from './useFormDataLoader';

import { useProfile } from '../api/useProfileApi';

import { createApiDataFromForm } from '../utils/formHelpers';

import { FORM_CONFIGS } from '../config/formFieldConfigs';

export const useDeliveryForm = (externalOnSubmit, onFormReady) => {
    const { getPersonalInfo, updatePersonalInfo } = useProfile();

    const { fieldConfig, initialValues } = FORM_CONFIGS.deliveryAddress;

    const handleSubmit = useCallback(
        async formData => {
            const apiData = createApiDataFromForm(formData, fieldConfig);

            try {
                const result = await updatePersonalInfo(apiData);

                if (result && !result.error) {
                    return { success: true };
                }

                if (result && typeof result === 'object') {
                    return {
                        success: false,
                        data: result,
                    };
                }
            } catch {
                return {
                    success: false,
                    error: 'Failed to update delivery information',
                };
            }
        },
        [fieldConfig, updatePersonalInfo]
    );

    const formProps = useForm(initialValues, {
        onSubmit: externalOnSubmit || handleSubmit,
        validateOnSubmit: true,
    });

    const { updateFieldValue, resetValidationStates, submitAction } = formProps;
    const { loading } = useFormDataLoader(getPersonalInfo, updateFieldValue, fieldConfig);

    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    useEffect(() => {
        if (onFormReady) {
            onFormReady({
                submitAction,
                formState: formProps.formState,
            });
        }
    }, [submitAction, formProps.formState, onFormReady]);

    return {
        formProps,
        fieldConfig,
        loading,
    };
};
