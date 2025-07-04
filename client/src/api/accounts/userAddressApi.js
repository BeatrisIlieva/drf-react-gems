import { useCallback } from 'react';
import { useApi } from '../../hooks/useApi';
import { HOST } from '../../constants/host';
import { keysToCamelCase } from '../../utils/convertToCamelCase';
import { keysToSnakeCase } from '../../utils/convertToSnakeCase';
import { useAuth } from '../../hooks/auth/useAuth';

const baseUrl = `${HOST}/api/accounts/address`;

export const useUserAddress = () => {
    const { get, patch } = useApi();
    const { isAuthenticated } = useAuth();

    const getUserAddress = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });

            return keysToCamelCase(response);
        } catch (error) {
            console.error(error);
            return {
                error: error.message || 'Failed to get address',
                ...error.data
            };
        }
    }, [get, isAuthenticated]);

    const updateUserAddress = useCallback(
        async (addressData) => {
            try {
                const response = await patch(`${baseUrl}/`, {
                    data: keysToSnakeCase(addressData),
                    accessRequired: isAuthenticated,
                    refreshRequired: isAuthenticated
                });
                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
                return {
                    error:
                        error.message ||
                        'Failed to update address',
                    ...error.data
                };
            }
        },
        [patch, isAuthenticated]
    );

    return {
        getUserAddress,
        updateUserAddress
    };
};
