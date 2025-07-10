import { useCallback, useState } from 'react';

import { useNavigate } from 'react-router';

import { useAuthentication } from '../api/authApi';

import { useUserContext } from '../contexts/UserContext';

import { createApiDataFromForm } from '../utils/formHelpers';

export const useRegister = fieldConfig => {
    const { userLoginHandler } = useUserContext();
    const { register, login } = useAuthentication();
    const navigate = useNavigate();

    const [agree, setAgree] = useState(true);
    const [agreeError, setAgreeError] = useState('');

    const validateAgreement = () => {
        if (!agree) {
            setAgreeError('You must agree to receive email updates.');
            return false;
        }
        setAgreeError('');
        return true;
    };

    const handleAuthResponse = async (authData, formData) => {
        if (authData?.access) {
            userLoginHandler(authData);

            await login({
                email_or_username: formData.email.value,
                password: formData.password.value,
            });

            navigate('/my-account/details');
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
    };

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
        [fieldConfig, register, login, userLoginHandler, navigate, agree]
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
