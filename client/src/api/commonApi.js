import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/common`;

export const useWakeUpServer = () => {
    const { get } = useApi();

    const wakeUpServer = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/wake-up-server/`);
            return response;
        } catch (error) {
            console.error(error);
        }
    }, [get]);

    return {
        wakeUpServer,
    };
};
