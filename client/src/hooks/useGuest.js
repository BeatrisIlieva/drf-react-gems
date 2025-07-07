import usePersistedState from './usePersistedState';

export const useGuest = () => {
    const [guestData, setGuestData] = usePersistedState(
        'guest',
        {}
    );

    const getGuestData = () => {
        // If we have a guest ID in state, use it
        if (guestData.guest_id) {
            return guestData.guest_id;
        }

        // Create a new guest ID only if we don't have one
        const guestId = crypto.randomUUID();
        setGuestData({ guest_id: guestId });

        return guestId;
    };

    const clearGuestData = () => {
        setGuestData({});
    };

    return {
        getGuestData,
        clearGuestData
    };
};


// import { useCallback, useRef } from 'react';
// import usePersistedState from './usePersistedState';

// export const useGuest = () => {
//     const [guestData, setGuestData] = usePersistedState(
//         'guest',
//         {}
//     );
//     const initializedRef = useRef(false);
//     let globalGuestId = null;

//     // Initialize global guest ID from persisted state
//     if (!initializedRef.current && guestData.guest_id) {
//         globalGuestId = guestData.guest_id;
//         initializedRef.current = true;
//     }

//     const getGuestData = useCallback(() => {
//         // If we have a global guest ID, use it
//         if (globalGuestId) {
//             return globalGuestId;
//         }

//         // If we have a guest ID in state, use it and cache it globally
//         if (guestData.guest_id) {
//             globalGuestId = guestData.guest_id;
//             return guestData.guest_id;
//         }

//         // Create a new guest ID only if we don't have one
//         const guestId = crypto.randomUUID();
//         globalGuestId = guestId;
//         setGuestData({ guest_id: guestId });

//         return guestId;
//     }, [guestData.guest_id, setGuestData]);

//     const clearGuestData = useCallback(() => {
//         globalGuestId = null;
//         setGuestData({});
//     }, [setGuestData]);

//     return {
//         getGuestData,
//         clearGuestData
//     };
// };



