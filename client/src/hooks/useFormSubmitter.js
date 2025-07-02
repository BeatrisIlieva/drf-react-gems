import { useCallback } from 'react';
import { 
    createApiDataFromForm
} from '../utils/formHelpers';

export const useFormSubmitter = (fieldConfig, apiUpdateFn, validateFields, handleServerSideErrors) => {
    const createSubmitHandler = useCallback((customValidation) => {
        return async (formData) => {
            const isValid = validateFields();
            
            if (!isValid) {
                return {
                    success: false,
                    error: 'Please fill in all required fields.'
                };
            }

            if (customValidation) {
                const customValidationResult = customValidation(formData);
                if (!customValidationResult.isValid) {
                    return {
                        success: false,
                        error: customValidationResult.error
                    };
                }
            }

            const apiData = createApiDataFromForm(formData, fieldConfig);

            try {
                const result = await apiUpdateFn(apiData);

                if (result && !result.error) {
                    return { success: true };
                }

                if (result && typeof result === 'object') {
                    handleServerSideErrors(result);
                }

                return {
                    success: false,
                    error: 'Failed to update information'
                };
            } catch {
                return {
                    success: false,
                    error: 'Failed to update information'
                };
            }
        };
    }, [fieldConfig, apiUpdateFn, validateFields, handleServerSideErrors]);

    return { createSubmitHandler };
};
