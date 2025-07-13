import { useCallback, useState } from 'react';

import { useLocation, useNavigate } from 'react-router';

import { useAuthentication } from '../api/authApi';

import { useUserContext } from '../contexts/UserContext';

import { createApiDataFromForm } from '../utils/formHelpers';

export const useLogin = fieldConfig => {
    const { userLoginHandler } = useUserContext();
    const { login } = useAuthentication();
    const navigate = useNavigate();
    const location = useLocation();

    const [invalidCredentials, setInvalidCredentials] = useState(false);

    const handleAuthResponse = authData => {
        if (authData?.access) {
            userLoginHandler(authData);

            const params = new URLSearchParams(location.search);
            const next = params.get('next');
            if (next) {
                navigate(next);
            } else {
                navigate('/my-account/details');
            }
            return { success: true };
        }

        if (!authData || authData === 'Invalid username or password') {
            setInvalidCredentials(true);
            return {
                success: false,
                error: 'Invalid username or password',
            };
        }

        if (authData && typeof authData === 'object' && !authData.access) {
            return {
                success: false,
                data: authData,
            };
        }

        return { success: false, error: 'Login failed' };
    };

    const handleSubmit = useCallback(
        async formData => {
            setInvalidCredentials(false);

            const apiData = createApiDataFromForm(formData, fieldConfig);
            const authData = await login(apiData);

            return handleAuthResponse(authData);
        },
        [fieldConfig, login, userLoginHandler, navigate, location]
    );

    return {
        handleSubmit,
        invalidCredentials,
    };
};
