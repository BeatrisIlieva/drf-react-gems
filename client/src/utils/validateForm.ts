import type { UserFormData } from '../types/User';
import { getFormFieldErrorMessage } from './getFormFieldErrorMessage';


interface ValidateFormResult {
    validatedUserData: UserFormData;
    isValid: boolean;
}

export const validateForm = (userData: UserFormData, updatedUserData: UserFormData): ValidateFormResult => {
    let isValid = true;

    Object.entries(userData).forEach(([field, fieldData]) => {
        if (!fieldData) return;
        
        const errorMessage = getFormFieldErrorMessage(field, fieldData.value);

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
