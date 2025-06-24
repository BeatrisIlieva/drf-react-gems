import { useState } from 'react';

import type { UserFormData, FormFieldState } from '../types/User';
import { validateForm } from '../utils/validateForm';
import { getFormFieldErrorMessage } from '../utils/getFormFieldErrorMessage';


interface UseFormReturn {
    userData: UserFormData;
    validateFields: () => boolean;
    validateField: (e: React.ChangeEvent<HTMLInputElement> | React.FocusEvent<HTMLInputElement>) => void;
    handleFieldChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
    setServerSideError: (serverData: Record<string, string[]>, field: string) => void;
    getInputClassName: (field: FormFieldState) => string;
}

export const useForm = (initialFormValues: UserFormData): UseFormReturn => {
    const [userData, setUserData] = useState<UserFormData>(initialFormValues);

    const validateFields = (): boolean => {
        const updatedUserData = { ...userData };

        const { validatedUserData, isValid } = validateForm(
            userData,
            updatedUserData
        );

        setUserData(validatedUserData);

        return isValid;
    };

    // This function validates a field on blur (existing behavior)
    const validateField = (e: React.ChangeEvent<HTMLInputElement> | React.FocusEvent<HTMLInputElement>): void => {
        const { name, value } = e.target;
        const error = getFormFieldErrorMessage(name, value);
        const valid = error === '';

        setUserData((state) => ({
            ...state,
            [name]: {
                value,
                error,
                valid
            }
        }));
    };
    
    // Function that validates in real-time as the user types
    // Shows valid (green) state immediately when valid, but only shows errors on blur
    const handleFieldChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
        const { name, value } = e.target;
        const error = getFormFieldErrorMessage(name, value);
        const valid = error === '';
        
        // Update the field in real-time
        setUserData((state) => ({
            ...state,
            [name]: {
                value,
                error: '', // Don't show error while typing
                valid: valid // Will be true if passes validation, showing green styling while typing
            }
        }));
    };

    const setServerSideError = (serverData: Record<string, string[]>, field: string): void => {
        if (serverData[field]) {
            setUserData((state) => ({
                ...state,
                [field]: {
                    error: serverData[field].join(' '),
                    value: state[field]?.value || '',
                    valid: false
                }
            }));
        }
    };

    // Updated to prioritize valid state over error state
    const getInputClassName = ({ error, valid }: FormFieldState): string => {
        if (valid) return 'valid';
        if (error) return 'invalid';
        return '';
    };

    return {
        userData,
        validateFields,
        validateField,
        handleFieldChange,
        setServerSideError,
        getInputClassName
    };
};
