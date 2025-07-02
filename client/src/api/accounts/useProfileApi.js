import { useCallback } from 'react';
import { useBaseApi } from '../../hooks/useBaseApi';
import { useApi } from '../../hooks/useApi';
import { useAuth } from '../../hooks/auth/useAuth';
import { HOST } from '../../constants/host';

const profileBaseUrl = `${HOST}/api/accounts/profile`;
const passwordBaseUrl = `${HOST}/api/accounts/change-password`;

export const useProfile = () => {
    const profileApi = useBaseApi(profileBaseUrl, { requireAuth: true });
    const { patch } = useApi();
    const { isAuthenticated } = useAuth();

    const getPersonalInfo = useCallback(async () => {
        return await profileApi.get();
    }, [profileApi]);

    const updatePersonalInfo = useCallback(async (personalData) => {
        try {
            const result = await profileApi.patch('', personalData);
            return result;
        } catch (error) {
            // Return error data for form handling
            return error.data;
        }
    }, [profileApi]);

    const changePassword = useCallback(async (passwordData) => {
        try {
            const result = await patch(`${passwordBaseUrl}/`, {
                data: passwordData,
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated
            });
            return result || { message: 'Password changed successfully' };
        } catch (error) {
            if (error?.status === 401) {
                return {
                    current_password: ['Current password is incorrect.'],
                    error: 'Current password is incorrect'
                };
            }
            return {
                error: error.message || 'Failed to change password',
                ...error.data
            };
        }
    }, [patch, isAuthenticated]);

    return {
        getPersonalInfo,
        updatePersonalInfo,
        changePassword
    };
};
