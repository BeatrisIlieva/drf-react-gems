import { useCallback, useState } from 'react';

import { useLocation, useNavigate } from 'react-router';

import { useAuthentication } from '../api/authApi';

import { useUserContext } from '../contexts/UserContext';

import { createApiDataFromForm } from '../utils/formHelpers';

export const useRegister = fieldConfig => {
    const { userLoginHandler } = useUserContext();
    const { register } = useAuthentication();
    const navigate = useNavigate();
    const location = useLocation();

    const [agree, setAgree] = useState(true);
    const [agreeError, setAgreeError] = useState('');

    const validateAgreement = useCallback(() => {
        if (!agree) {
            setAgreeError('You must agree to receive email updates.');
            return false;
        }
        setAgreeError('');
        return true;
    }, [agree]);

    const handleAuthResponse = useCallback(
        async authData => {
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

            if (authData && typeof authData === 'object' && !authData.access) {
                return {
                    success: false,
                    error: 'Registration failed',
                    data: authData,
                };
            }

            return {
                success: false,
                error: 'Registration failed',
            };
        },
        [userLoginHandler, navigate, location]
    );

    const handleSubmit = useCallback(
        async formData => {
            if (!validateAgreement()) {
                return { success: false };
            }

            const apiData = {
                ...createApiDataFromForm(formData, fieldConfig),
                agreed_to_emails: true,
            };

            const authData = await register(apiData);
            return handleAuthResponse(authData, formData);
        },
        [fieldConfig, register, handleAuthResponse, validateAgreement]
    );

    const toggleAgreement = () => {
        setAgree(!agree);
        if (agreeError) setAgreeError('');
    };

    return {
        handleSubmit,
        agree,
        agreeError,
        toggleAgreement,
        validateAgreement,
    };
};
