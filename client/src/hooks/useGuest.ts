import { useCallback } from 'react';
import usePersistedState from './usePersistedState';

interface GuestData {
    guest_id?: string;
}

interface UseGuestReturn {
    getGuestData: () => string | undefined;
    clearGuestData: () => void;
}

export const useGuest = (): UseGuestReturn => {
    const [guestData, setGuestData] = usePersistedState<GuestData>('guest', {});

    const getGuestData = useCallback(() => {
        if (!guestData.guest_id) {
            const guestId = crypto.randomUUID();

            setGuestData({ guest_id: guestId });
        }

        return guestData.guest_id;
    }, [guestData.guest_id, setGuestData]);

    const clearGuestData = useCallback(() => {
        setGuestData({});
    }, [setGuestData]);

    return {
        getGuestData,
        clearGuestData
    };
};
