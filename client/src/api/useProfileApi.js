import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const profileBaseUrl = `${HOST}/api/accounts/profile`;
const passwordBaseUrl = `${HOST}/api/accounts/change-password`;

export const useProfile = () => {
    const { get, patch } = useApi();
    const { isAuthenticated } = useAuth();

    const getPersonalInfo = useCallback(async () => {
        try {
            const response = await get(`${profileBaseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
            return {
                error: error.message || 'Failed to get personal information',
                ...error.data,
            };
        }
    }, [get, isAuthenticated]);

    const updatePersonalInfo = useCallback(
        async personalData => {
            try {
                const response = await patch(`${profileBaseUrl}/`, {
                    data: personalData,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
                return {
                    error: error.message || 'Failed to update personal information',
                    ...error.data,
                };
            }
        },
        [patch, isAuthenticated]
    );

    const changePassword = useCallback(
        async passwordData => {
            try {
                const result = await patch(`${passwordBaseUrl}/`, {
                    data: passwordData,
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated,
                });
                return (
                    result || {
                        message: 'Password changed successfully',
                    }
                );
            } catch (error) {
                if (error?.status === 401) {
                    return {
                        current_password: ['Current password is incorrect.'],
                        error: 'Current password is incorrect',
                    };
                }
                return {
                    error: error.message || 'Failed to change password',
                    ...error.data,
                };
            }
        },
        [patch, isAuthenticated]
    );

    return {
        getPersonalInfo,
        updatePersonalInfo,
        changePassword,
    };
};
