import { useCallback } from 'react';
import { usePersistedState } from './usePersistedState';

interface GuestData {
    guest_id?: string;
}

export const useGuest = () => {
    const [guestData, setGuestData] = usePersistedState<GuestData>('guest', {});

    const getGuestData = useCallback((): string | undefined => {
        if (!guestData.guest_id) {
            const guestId = crypto.randomUUID();
            setGuestData({ guest_id: guestId });
            return guestId;
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
