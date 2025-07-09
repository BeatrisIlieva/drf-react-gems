import { useCallback } from 'react';

import usePersistedState from './usePersistedState';

let globalGuestId = null;
let isGenerating = false;

export const useGuest = () => {
    const [guestData, setGuestData] = usePersistedState('guest', {});

    const getGuestData = useCallback(() => {
        if (globalGuestId) {
            return globalGuestId;
        }

        if (guestData.guest_id) {
            globalGuestId = guestData.guest_id;
            return guestData.guest_id;
        }

        if (isGenerating) {
            return null;
        }

        isGenerating = true;
        const guestId = crypto.randomUUID();
        globalGuestId = guestId;
        setGuestData({ guest_id: guestId });
        isGenerating = false;

        return guestId;
    }, [guestData.guest_id, setGuestData]);

    const clearGuestData = useCallback(() => {
        globalGuestId = null;
        setGuestData({});
    }, [setGuestData]);

    return {
        getGuestData,
        clearGuestData,
    };
};
