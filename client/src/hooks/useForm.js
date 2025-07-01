import { useState, useActionState, useCallback } from 'react';

import { validateForm } from '../utils/validateForm';
import { getFormFieldErrorMessage } from '../utils/getFormFieldErrorMessage';

export const useForm = (initialFormValues, options) => {
    const {
        validateOnSubmit = true,
        resetOnSuccess = false,
        onSubmit
    } = options;

    const [formData, setFormData] =
        useState(initialFormValues);
    const [interactedFields, setInteractedFields] = useState(
        new Set()
    );

    const handleFormSubmission = async () => {
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
    const updateFieldValue = useCallback(
        (fieldName, value, markAsInteracted) => {
            setFormData((state) => ({
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
            }));

            if (markAsInteracted) {
                setInteractedFields((prev) =>
                    new Set(prev).add(fieldName)
                );
            }
        },
        []
    );

    const validateFields = () => {
        const updatedFormData = { ...formData };

        const { validatedUserData, isValid } = validateForm(
            formData,
            updatedFormData
        );

        setFormData(validatedUserData);

        return isValid;
    };

    // This function validates a field on blur and marks it as interacted
    const validateField = (e) => {
        const { name, value } = e.target;
        const error = getFormFieldErrorMessage(name, value);
        const valid = error === '';

        // Mark field as interacted when validation occurs (on blur)
        setInteractedFields((prev) => new Set(prev).add(name));

        setFormData((state) => ({
            ...state,
            [name]: {
                value,
                error,
                valid
            }
        }));
    };

    // Function that updates field value as user types
    // Shows valid state in real-time when field passes validation
    const handleFieldChange = (e) => {
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
        setFormData((state) => ({
            ...state,
            [name]: {
                value,
                error: '', // Don't show error while typing
                valid: shouldShowValid
            }
        }));
    };

    const setServerSideError = useCallback(
        (serverData, field) => {
            if (serverData[field]) {
                setFormData((state) => ({
                    ...state,
                    [field]: {
                        error: serverData[field].join(' '),
                        value: state[field]?.value || '',
                        valid: false
                    }
                }));
            }
        },
        []
    );

    // Updated to prioritize valid state over error state
    const getInputClassName = ({ error, valid }) => {
        if (valid) return 'valid';
        if (error) return 'invalid';
        return '';
    };

    const resetForm = () => {
        setFormData(initialFormValues);
        setInteractedFields(new Set());
    };

    const resetValidationStates = useCallback(() => {
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
