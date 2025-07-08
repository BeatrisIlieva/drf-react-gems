import { useCallback } from 'react';
import usePersistedState from './usePersistedState';

// Global variable to ensure singleton behavior
let globalGuestId = null;
let isGenerating = false;

export const useGuest = () => {
    const [guestData, setGuestData] = usePersistedState(
        'guest',
        {}
    );

    const getGuestData = useCallback(() => {
        // If we have a cached global guest ID, use it
        if (globalGuestId) {
            return globalGuestId;
        }

        // If we have a guest ID in persisted state, cache it and use it
        if (guestData.guest_id) {
            globalGuestId = guestData.guest_id;
            return guestData.guest_id;
        }

        // Prevent multiple simultaneous UUID generation
        if (isGenerating) {
            // Return null temporarily, the component should retry
            return null;
        }

        // Create a new guest ID only if we don't have one
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
        clearGuestData
    };
};



