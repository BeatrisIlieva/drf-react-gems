import { useState } from 'react';
import type { LoginFormData, FormFieldState } from '../types/User';
import { validateForm } from '../utils/validateForm';
import { getFormFieldErrorMessage } from '../utils/getFormFieldErrorMessage';

interface UseLoginFormReturn {
    loginData: LoginFormData;
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

export const useLoginForm = (
    initialFormValues: LoginFormData
): UseLoginFormReturn => {
    const [loginData, setLoginData] = useState<LoginFormData>(
        initialFormValues
    );

    const validateFields = (): boolean => {
        const updatedLoginData = { ...loginData };

        const { validatedUserData, isValid } = validateForm(
            loginData,
            updatedLoginData
        );

        setLoginData(validatedUserData as LoginFormData);

        return isValid;
    };

    const validateField = (
        e:
            | React.ChangeEvent<HTMLInputElement>
            | React.FocusEvent<HTMLInputElement>
    ): void => {
        const { name, value } = e.target;

        const errorMessage = getFormFieldErrorMessage(name, value);

        setLoginData((prevData) => {
            const field = prevData[name as keyof LoginFormData];
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

        setLoginData((prevData) => {
            const field = prevData[name as keyof LoginFormData];
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
            setLoginData((prevData) => {
                const fieldData = prevData[field as keyof LoginFormData];
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
        loginData,
        validateFields,
        validateField,
        handleFieldChange,
        setServerSideError,
        getInputClassName
    };
};
