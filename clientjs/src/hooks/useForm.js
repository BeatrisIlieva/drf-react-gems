import { useState } from 'react';

import { validateForm } from '../utils/validateForm';
import { validators } from '../utils/getFormFieldErrorMessage';

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

        let error;
        for (const validationFn of Object.values(validators[name])) {
            error = validationFn(value);
        }

        setUserData((state) => ({
            ...state,
            [name]: {
                value,
                error
            }
        }));
    };

    const changeHandler = (e) => {
        const { name, value } = e.target;

        setUserData((state) => ({
            ...state,
            [name]: {
                value,
                error: ''
            }
        }));
    };

    const setServerSideError = (serverData, field) => {
        if (serverData[field]) {
            setUserData((state) => ({
                ...state,
                [field]: {
                    error: serverData[field].join(' '),
                    value: state[field].value
                }
            }));
        }
    };

    // const setServerSideError = (serverData) => {
    //     setUserData((state) => {
    //         const newState = { ...state };
    
    //         Object.keys(serverData).forEach((key) => {
    //             if (newState[key]) {
    //                 newState[key] = {
    //                     ...newState[key],
    //                     error: serverData[key].join(' ')
    //                 };
    //             }
    //         });
    
    //         return newState;
    //     });
    // };

    return {
        userData,
        validateFields,
        validateField,
        changeHandler,
        setServerSideError
    };
};
