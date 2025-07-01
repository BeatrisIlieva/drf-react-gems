import { useCallback } from 'react';

export const useServerSideErrors = (setFormData, initialFormValues) => {
    const handleServerSideErrors = useCallback(
        (serverResponse) => {
            if (!serverResponse || typeof serverResponse !== 'object') {
                return false;
            }

            let hasErrors = false;

            // Check if server response contains field-specific errors
            Object.keys(initialFormValues).forEach((fieldName) => {
                if (serverResponse[fieldName]) {
                    hasErrors = true;
                    setFormData((state) => ({
                        ...state,
                        [fieldName]: {
                            ...state[fieldName],
                            error: Array.isArray(serverResponse[fieldName])
                                ? serverResponse[fieldName].join(' ')
                                : serverResponse[fieldName],
                            valid: false
                        }
                    }));
                }
            });

            // Handle snake_case to camelCase mapping for common field names
            const fieldMapping = {
                current_password: 'currentPassword',
                new_password: 'newPassword',
                email_or_username: 'email_or_username'
            };

            Object.entries(fieldMapping).forEach(([serverFieldName, clientFieldName]) => {
                if (serverResponse[serverFieldName] && initialFormValues[clientFieldName]) {
                    hasErrors = true;
                    setFormData((state) => ({
                        ...state,
                        [clientFieldName]: {
                            ...state[clientFieldName],
                            error: Array.isArray(serverResponse[serverFieldName])
                                ? serverResponse[serverFieldName].join(' ')
                                : serverResponse[serverFieldName],
                            valid: false
                        }
                    }));
                }
            });

            return hasErrors;
        },
        [setFormData, initialFormValues]
    );

    return { handleServerSideErrors };
};
