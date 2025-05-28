import { useCallback } from 'react';
import usePersistedState from './usePersistedState';

export const useGuest = () => {
    const [guestData, setGuestData] = usePersistedState('guest', {});

    const getGuestData = useCallback(() => {
        if (!guestData.guest_id) {
            const guestId = crypto.randomUUID();

            setGuestData({ guest_id: guestId });
        }

        return guestData.guest_id;
    }, [guestData.guest_id, setGuestData]);

    return {
        getGuestData
    };
};
