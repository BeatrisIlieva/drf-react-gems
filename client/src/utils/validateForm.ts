import type { UserFormData, LoginFormData, RegisterFormData } from '../types/User';
import { getFormFieldErrorMessage } from './getFormFieldErrorMessage';

type AnyFormData = UserFormData | LoginFormData | RegisterFormData;

interface ValidateFormResult<T extends AnyFormData> {
    validatedUserData: T;
    isValid: boolean;
}

export const validateForm = <T extends AnyFormData>(
    userData: T, 
    updatedUserData: T
): ValidateFormResult<T> => {
    let isValid = true;

    Object.entries(userData).forEach(([field, fieldData]) => {
        if (!fieldData) return;
        
        const errorMessage = getFormFieldErrorMessage(field, fieldData.value);

        if (errorMessage !== '') {
            isValid = false;
        }

        (updatedUserData as Record<string, unknown>)[field] = {
            ...fieldData,
            error: errorMessage,
            valid: errorMessage === ''
        };
    });

    return { validatedUserData: updatedUserData, isValid };
};
