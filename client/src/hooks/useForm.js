import { useActionState, useCallback, useState } from 'react';

import { useFocusOnInvalidInput } from './useFocusOnInvalidInput';

import { getFormFieldErrorMessage } from '../utils/getFormFieldErrorMessage';

export const useForm = (initialFormValues, options = {}) => {
    const { validateOnSubmit = true, resetOnSuccess = false, onSubmit, customValidation } = options;

    const [formData, setFormData] = useState(initialFormValues);
    const [interactedFields, setInteractedFields] = useState(new Set());

    const { formRef, registerInput, focusFirstInvalid } = useFocusOnInvalidInput();

    const handleFormSubmission = async () => {
        if (validateOnSubmit) {
            const isValid = validateFields();
            if (!isValid) {
                return {
                    success: false,
                    error: 'Form validation failed',
                };
            }
        }

        if (onSubmit) {
            const result = await onSubmit(formData);

            if (!result.success && result.data) {
                handleServerSideErrors(result.data);
            }

            if (result.success && resetOnSuccess) {
                resetForm();
            }
            return result;
        }

        return { success: true };
    };

    const [formState, submitFormAction, isSubmitting] = useActionState(handleFormSubmission, null);

    const submitAction = submitFormAction;

    const updateFieldValue = useCallback(
        (fieldName, value, markAsInteracted, preserveError = false) => {
            const error = customValidation
                ? customValidation(fieldName, value)
                : getFormFieldErrorMessage(fieldName, value);

            setFormData(state => ({
                ...state,
                [fieldName]: {
                    value,
                    error: preserveError ? state[fieldName]?.error || '' : '',
                    valid: markAsInteracted ? error === '' : false,
                },
            }));

            if (markAsInteracted) {
                setInteractedFields(prev => new Set(prev).add(fieldName));
            }
        },
        [customValidation]
    );

    const validateFields = useCallback(() => {
        const updatedFormData = { ...formData };
        let isValid = true;

        Object.entries(formData).forEach(([field, fieldData]) => {
            if (!fieldData) return;

            const errorMessage = customValidation
                ? customValidation(field, fieldData.value)
                : getFormFieldErrorMessage(field, fieldData.value);

            if (errorMessage !== '') {
                isValid = false;
            }

            updatedFormData[field] = {
                ...fieldData,
                error: errorMessage,
                valid: errorMessage === '',
            };
        });

        setFormData(updatedFormData);

        if (!isValid) {
            focusFirstInvalid(updatedFormData);
        }

        return isValid;
    }, [formData, customValidation, focusFirstInvalid]);

    const validateField = e => {
        const { name, value } = e.target;
        const error = customValidation
            ? customValidation(name, value)
            : getFormFieldErrorMessage(name, value);
        const valid = error === '';

        setInteractedFields(prev => new Set(prev).add(name));

        setFormData(state => ({
            ...state,
            [name]: {
                value,
                error,
                valid,
            },
        }));
    };

    const handleFieldChange = e => {
        const { name, value } = e.target;
        const error = customValidation
            ? customValidation(name, value)
            : getFormFieldErrorMessage(name, value);
        const isFieldValid = error === '';
        const hasInteracted = interactedFields.has(name);

        const shouldShowValid =
            (hasInteracted && isFieldValid) || (String(value).trim() !== '' && isFieldValid);

        setFormData(state => ({
            ...state,
            [name]: {
                value,
                error: isFieldValid ? '' : state[name]?.error || '',
                valid: shouldShowValid,
            },
        }));
    };

    const handleServerSideErrors = useCallback(
        serverResponse => {
            if (!serverResponse || typeof serverResponse !== 'object') {
                return false;
            }

            let hasErrors = false;
            let updatedFormData = {};

            Object.keys(initialFormValues).forEach(fieldName => {
                if (serverResponse[fieldName]) {
                    hasErrors = true;
                    updatedFormData[fieldName] = {
                        error: Array.isArray(serverResponse[fieldName])
                            ? serverResponse[fieldName].join(' ')
                            : serverResponse[fieldName],
                        valid: false,
                    };
                }
            });

            const fieldMapping = {
                current_password: 'currentPassword',
                new_password: 'newPassword',
                email_or_username: 'email_or_username',
                first_name: 'firstName',
                last_name: 'lastName',
                phone_number: 'phoneNumber',
            };

            Object.entries(fieldMapping).forEach(([serverFieldName, clientFieldName]) => {
                if (serverResponse[serverFieldName] && initialFormValues[clientFieldName]) {
                    hasErrors = true;
                    updatedFormData[clientFieldName] = {
                        error: Array.isArray(serverResponse[serverFieldName])
                            ? serverResponse[serverFieldName].join(' ')
                            : serverResponse[serverFieldName],
                        valid: false,
                    };
                }
            });

            if (hasErrors) {
                setFormData(state => {
                    const newState = { ...state };
                    Object.keys(updatedFormData).forEach(fieldName => {
                        if (newState[fieldName]) {
                            newState[fieldName] = {
                                ...newState[fieldName],
                                ...updatedFormData[fieldName],
                            };
                        }
                    });

                    setTimeout(() => {
                        focusFirstInvalid(newState);
                    }, 0);

                    return newState;
                });
            }

            return hasErrors;
        },
        [initialFormValues, focusFirstInvalid]
    );

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
        setFormData(state => {
            const resetState = { ...state };
            for (const key in resetState) {
                if (resetState[key]) {
                    resetState[key] = {
                        ...resetState[key],
                        valid: false,
                        error: '',
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

        handleServerSideErrors,
        getInputClassName,
        setFormData,
        resetForm,
        submitAction,
        isSubmitting,
        formState,
        updateFieldValue,
        interactedFields,
        resetValidationStates,
        formRef,
        registerInput,
    };
};
