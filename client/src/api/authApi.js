import { useCallback } from 'react';

import { useNavigate } from 'react-router';

import { useApi } from '../hooks/useApi';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/accounts`;

export const useAuthentication = () => {
    const { post, del } = useApi();
    const navigate = useNavigate();

    const register = useCallback(
        async userData => {
            try {
                const response = await post(`${baseUrl}/register/`, {
                    data: userData,
                });
                return response;
            } catch (error) {
                console.error(error);
                return {
                    error: error.message || 'Registration failed',
                    ...error.data,
                };
            }
        },
        [post]
    );

    const login = useCallback(
        async userData => {
            try {
                const response = await post(`${baseUrl}/login/`, {
                    data: userData,
                });
                return response;
            } catch (error) {
                console.error(error);
                return {
                    error: error.message || 'Login failed',
                    ...error.data,
                };
            }
        },
        [post]
    );

    const logout = useCallback(async () => {
        try {
            await post(`${baseUrl}/logout/`, {
                accessRequired: true,
                refreshRequired: true,
            });
            navigate('/my-account/register');
        } catch (error) {
            console.error(error);
        }
    }, [post, navigate]);

    const deleteUser = useCallback(async () => {
        try {
            const response = await del(`${baseUrl}/delete/`, {
                accessRequired: true,
                refreshRequired: true,
            });
            return response;
        } catch (error) {
            console.error(error);
        }
    }, [del]);

    return {
        register,
        login,
        logout,
        deleteUser,
    };
};
