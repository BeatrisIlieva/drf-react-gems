import { getFormFieldErrorMessage } from './getFormFieldErrorMessage';

export const validateFormFields = (userData, updatedUserData) => {
    let isValid = true;

    Object.entries(userData).forEach(([field, fieldData]) => {
        const errorMessage = getFormFieldErrorMessage(field, fieldData.value);

        if (errorMessage !== '') {
            isValid = false;
        }

        updatedUserData[field] = {
            ...fieldData,
            error: errorMessage
        };
    });


    return { validatedUserData: updatedUserData, isValid };
};
