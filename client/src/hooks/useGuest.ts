import { useCallback, useRef } from 'react';
import usePersistedState from './usePersistedState';

interface GuestData {
    guest_id?: string;
}

interface UseGuestReturn {
    getGuestData: () => string;
    clearGuestData: () => void;
}

let globalGuestId: string | null = null;

export const useGuest = (): UseGuestReturn => {
    const [guestData, setGuestData] = usePersistedState<GuestData>('guest', {});
    const initializedRef = useRef(false);

    // Initialize global guest ID from persisted state
    if (!initializedRef.current && guestData.guest_id) {
        globalGuestId = guestData.guest_id;
        initializedRef.current = true;
    }

    const getGuestData = useCallback((): string => {
        // If we have a global guest ID, use it
        if (globalGuestId) {
            return globalGuestId;
        }

        // If we have a guest ID in state, use it and cache it globally
        if (guestData.guest_id) {
            globalGuestId = guestData.guest_id;
            return guestData.guest_id;
        }

        // Create a new guest ID only if we don't have one
        const guestId = crypto.randomUUID();
        globalGuestId = guestId;
        setGuestData({ guest_id: guestId });
        
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
