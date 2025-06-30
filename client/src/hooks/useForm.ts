import { useState, useActionState, useCallback } from 'react';

import type {
    FormData,
    FormFieldState,
    FormSubmissionResult
} from '../types/User';
import { validateForm } from '../utils/validateForm';
import { getFormFieldErrorMessage } from '../utils/getFormFieldErrorMessage';

interface UseFormOptions<T extends FormData> {
    validateOnSubmit?: boolean;
    resetOnSuccess?: boolean;
    onSubmit?: (formData: T) => Promise<FormSubmissionResult>;
}

interface UseFormReturn<T extends FormData> {
    formData: T;
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
    setFormData: React.Dispatch<React.SetStateAction<T>>;
    resetForm: () => void;
    resetValidationStates: () => void;
    // React 19 useActionState integration
    submitAction: () => void; // For form action prop
    isSubmitting: boolean;
    formState: FormSubmissionResult | null;
    // Helper to update specific field values (for loading data from server)
    updateFieldValue: (
        fieldName: string,
        value: string,
        markAsInteracted?: boolean
    ) => void;
    // Track field interaction for proper validation styling
    interactedFields: Set<string>;
}

export const useForm = <T extends FormData>(
    initialFormValues: T,
    options: UseFormOptions<T> = {}
): UseFormReturn<T> => {
    const {
        validateOnSubmit = true,
        resetOnSuccess = false,
        onSubmit
    } = options;

    const [formData, setFormData] = useState<T>(
        initialFormValues
    );
    const [interactedFields, setInteractedFields] = useState<
        Set<string>
    >(new Set());

    // Async action handler for useActionState
    const handleFormSubmission = async (
        // eslint-disable-next-line @typescript-eslint/no-unused-vars
        _prevState: FormSubmissionResult | null
    ): Promise<FormSubmissionResult> => {
        if (validateOnSubmit) {
            const isValid = validateFields();
            if (!isValid) {
                return {
                    success: false,
                    error: 'Form validation failed'
                };
            }
        }

        if (onSubmit) {
            const result = await onSubmit(formData);
            if (result.success && resetOnSuccess) {
                resetForm();
            }
            return result;
        }

        return { success: true };
    };

    // React 19 useActionState for form submission
    const [formState, submitFormAction, isSubmitting] =
        useActionState(handleFormSubmission, null);

    // The submitAction is the function returned from useActionState
    const submitAction = submitFormAction;

    // Helper function to update field values (e.g., when loading from server)
    const updateFieldValue = useCallback((
        fieldName: string,
        value: string,
        markAsInteracted: boolean = false
    ): void => {
        setFormData(
            (state) =>
                ({
                    ...state,
                    [fieldName]: {
                        value,
                        error: '',
                        valid: markAsInteracted
                            ? getFormFieldErrorMessage(
                                  fieldName,
                                  value
                              ) === ''
                            : false
                    }
                }) as T
        );

        if (markAsInteracted) {
            setInteractedFields((prev) =>
                new Set(prev).add(fieldName)
            );
        }
    }, []);

    const validateFields = (): boolean => {
        const updatedFormData = { ...formData };

        const { validatedUserData, isValid } = validateForm(
            formData,
            updatedFormData
        );

        setFormData(validatedUserData as T);

        return isValid;
    };

    // This function validates a field on blur and marks it as interacted
    const validateField = (
        e:
            | React.ChangeEvent<HTMLInputElement>
            | React.FocusEvent<HTMLInputElement>
    ): void => {
        const { name, value } = e.target;
        const error = getFormFieldErrorMessage(name, value);
        const valid = error === '';

        // Mark field as interacted when validation occurs (on blur)
        setInteractedFields((prev) => new Set(prev).add(name));

        setFormData(
            (state) =>
                ({
                    ...state,
                    [name]: {
                        value,
                        error,
                        valid
                    }
                }) as T
        );
    };

    // Function that updates field value as user types
    // Shows valid state in real-time when field passes validation
    const handleFieldChange = (
        e: React.ChangeEvent<HTMLInputElement>
    ): void => {
        const { name, value } = e.target;
        const error = getFormFieldErrorMessage(name, value);
        const isFieldValid = error === '';
        const hasInteracted = interactedFields.has(name);

        // Show valid state if:
        // 1. Field has been interacted with before (blurred), OR
        // 2. Field has value and is valid (real-time validation feedback)
        const shouldShowValid =
            (hasInteracted && isFieldValid) ||
            (value.trim() !== '' && isFieldValid);

        // Update the field in real-time
        setFormData(
            (state) =>
                ({
                    ...state,
                    [name]: {
                        value,
                        error: '', // Don't show error while typing
                        valid: shouldShowValid
                    }
                }) as T
        );
    };

    const setServerSideError = useCallback((
        serverData: Record<string, string[]>,
        field: string
    ): void => {
        if (serverData[field]) {
            setFormData(
                (state) =>
                    ({
                        ...state,
                        [field]: {
                            error: serverData[field].join(' '),
                            value: state[field]?.value || '',
                            valid: false
                        }
                    }) as T
            );
        }
    }, []);

    // Updated to prioritize valid state over error state
    const getInputClassName = ({
        error,
        valid
    }: FormFieldState): string => {
        if (valid) return 'valid';
        if (error) return 'invalid';
        return '';
    };

    const resetForm = (): void => {
        setFormData(initialFormValues);
        setInteractedFields(new Set());
    };

    const resetValidationStates = useCallback((): void => {
        setFormData((state) => {
            const resetState = { ...state };
            for (const key in resetState) {
                if (resetState[key]) {
                    resetState[key] = {
                        ...resetState[key],
                        valid: false,
                        error: ''
                    };
                }
            }
            return resetState;
        });
        setInteractedFields(new Set());
    }, []);

    return {
        formData,
        validateFields,
        validateField,
        handleFieldChange,
        setServerSideError,
        getInputClassName,
        setFormData,
        resetForm,
        submitAction,
        isSubmitting,
        formState,
        updateFieldValue,
        interactedFields,
        resetValidationStates
    };
};
