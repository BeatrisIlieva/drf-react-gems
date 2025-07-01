import { getFormFieldErrorMessage } from './getFormFieldErrorMessage';

export const validateForm = (userData, updatedUserData) => {
    let isValid = true;

    Object.entries(userData).forEach(([field, fieldData]) => {
        if (!fieldData) return;

        const errorMessage = getFormFieldErrorMessage(
            field,
            fieldData.value
        );

        if (errorMessage !== '') {
            isValid = false;
        }

        updatedUserData[field] = {
            ...fieldData,
            error: errorMessage,
            valid: errorMessage === ''
        };
    });

    return { validatedUserData: updatedUserData, isValid };
};
