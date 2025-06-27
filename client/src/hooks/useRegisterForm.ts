import { useState } from 'react';
import type { RegisterFormData, FormFieldState } from '../types/User';
import { validateForm } from '../utils/validateForm';
import { getFormFieldErrorMessage } from '../utils/getFormFieldErrorMessage';

interface UseRegisterFormReturn {
    registerData: RegisterFormData;
    validateFields: () => boolean;
    validateField: (
        e:
            | React.ChangeEvent<HTMLInputElement>
            | React.FocusEvent<HTMLInputElement>
    ) => void;
    handleFieldChange: (
        e: React.ChangeEvent<HTMLInputElement>
    ) => void;
    setServerSideError: (
        serverData: Record<string, string[]>,
        field: string
    ) => void;
    getInputClassName: (field: FormFieldState) => string;
}

export const useRegisterForm = (
    initialFormValues: RegisterFormData
): UseRegisterFormReturn => {
    const [registerData, setRegisterData] = useState<RegisterFormData>(
        initialFormValues
    );

    const validateFields = (): boolean => {
        const updatedRegisterData = { ...registerData };

        const { validatedUserData, isValid } = validateForm(
            registerData,
            updatedRegisterData
        );

        setRegisterData(validatedUserData as RegisterFormData);

        return isValid;
    };

    const validateField = (
        e:
            | React.ChangeEvent<HTMLInputElement>
            | React.FocusEvent<HTMLInputElement>
    ): void => {
        const { name, value } = e.target;

        const errorMessage = getFormFieldErrorMessage(name, value);

        setRegisterData((prevData) => {
            const field = prevData[name as keyof RegisterFormData];
            if (!field) return prevData;
            
            return {
                ...prevData,
                [name]: {
                    ...field,
                    error: errorMessage,
                    valid: errorMessage === ''
                }
            };
        });
    };

    const handleFieldChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ): void => {
        const { name, value } = e.target;
        const error = getFormFieldErrorMessage(name, value);
        const valid = error === '';

        setRegisterData((prevData) => {
            const field = prevData[name as keyof RegisterFormData];
            if (!field) return prevData;
            
            return {
                ...prevData,
                [name]: {
                    ...field,
                    value,
                    error: '', // Don't show error while typing
                    valid: valid // Will be true if passes validation, showing green styling while typing
                }
            };
        });
    };

    const setServerSideError = (
        serverData: Record<string, string[]>,
        field: string
    ): void => {
        if (serverData[field]) {
            setRegisterData((prevData) => {
                const fieldData = prevData[field as keyof RegisterFormData];
                if (!fieldData) return prevData;
                
                return {
                    ...prevData,
                    [field]: {
                        ...fieldData,
                        error: serverData[field][0],
                        valid: false
                    }
                };
            });
        }
    };

    const getInputClassName = (field: FormFieldState): string => {
        if (field.valid && field.value.length > 0) return 'valid';
        if (field.error && !field.valid) return 'invalid';
        return '';
    };

    return {
        registerData,
        validateFields,
        validateField,
        handleFieldChange,
        setServerSideError,
        getInputClassName
    };
};
