import usePersistedState from './usePersistedState';

export const useGuest = () => {
    const [guestData, setGuestData] = usePersistedState('guest', {});

    const setGuestDataHandler = () => {
        if (!guestData.guest_id) {
            const guestId = crypto.randomUUID();

            setGuestData({'guest_id': guestId})
        }
    };

    return {
        guestId: guestData.guest_id,
        setGuestDataHandler
    };
};
