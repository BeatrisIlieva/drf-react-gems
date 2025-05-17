import { useState } from 'react';

import { validateForm } from '../utils/validateForm';
import { getFormFieldErrorMessage } from '../utils/getFormFieldErrorMessage';

export const useForm = (initialFormValues) => {
    const [userData, setUserData] = useState(initialFormValues);

    const validateFields = () => {
        let updatedUserData = { ...userData };

        const { validatedUserData, isValid } = validateForm(
            userData,
            updatedUserData
        );

        setUserData(validatedUserData);

        return isValid;
    };

    const validateField = (e) => {
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


    const setServerSideError = (serverData, field) => {
        if (serverData[field]) {
            setUserData((state) => ({
                ...state,
                [field]: {
                    error: serverData[field].join(' '),
                    value: state[field].value,
                    valid: false
                }
            }));
        }
    };

    const getInputClassName = ({ error, valid }) =>
        `${error ? 'invalid' : valid ? 'valid' : ''}`.trim();

    return {
        userData,
        validateFields,
        validateField,
        setServerSideError,
        getInputClassName
    };
};
