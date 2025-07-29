import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const profileBaseUrl = `${HOST}/api/accounts/profile`;
const passwordBaseUrl = `${HOST}/api/accounts/change-password`;

export const useProfile = () => {
    const { get, patch } = useApi();

    const getPersonalInfo = useCallback(async () => {
        try {
            const response = await get(`${profileBaseUrl}/`, {
                accessRequired: true,
                refreshRequired: true,
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
            return {
                error: error.message || 'Failed to get personal information',
                ...error.data,
            };
        }
    }, [get]);

    const updatePersonalInfo = useCallback(
        async personalData => {
            try {
                const response = await patch(`${profileBaseUrl}/`, {
                    data: personalData,
                    accessRequired: true,
                    refreshRequired: true,
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
        [patch]
    );

    const changePassword = useCallback(
        async passwordData => {
            try {
                const result = await patch(`${passwordBaseUrl}/`, {
                    data: passwordData,
                    accessRequired: true,
                    refreshRequired: true,
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
        [patch]
    );

    return {
        getPersonalInfo,
        updatePersonalInfo,
        changePassword,
    };
};
