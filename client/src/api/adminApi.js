import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';
import { useAuth } from '../hooks/useAuth';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/common`;

export const useAdmin = () => {
    const { get } = useApi();
    const { isAuthenticated } = useAuth();

    const sendReminder = useCallback(async () => {
        try {
            await get(`${baseUrl}/admin-page/`);
            return { success: true };
        } catch (error) {
            console.error(error);
        }
    }, [get]);

    const getBagReminderInfo = useCallback(async () => {
        try {
            return await get(`${baseUrl}/admin-bag-info/`, {
                accessRequired: isAuthenticated,
                refreshRequired: isAuthenticated,
            });
        } catch (error) {
            console.error(error);
            return null;
        }
    }, [get, isAuthenticated]);

    return {
        sendReminder,
        getBagReminderInfo,
    };
};
