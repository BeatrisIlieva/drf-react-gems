import { UserContext } from '../contexts/UserContext';
import usePersistedState from '../hooks/usePersistedState';

import { useGuest } from '../hooks/useGuest';

export const UserProvider = ({ children }) => {
    const [authData, setAuthData] = usePersistedState('auth', {});
    const { clearGuestData } = useGuest();

    const userLoginHandler = (resultData) => {
        setAuthData(resultData);
    };

    const userLogoutHandler = () => {
        setAuthData({});
        clearGuestData();
    };

    return (
        <UserContext.Provider
            value={{
                ...authData,
                userLoginHandler,
                userLogoutHandler
            }}
        >
            {children}
        </UserContext.Provider>
    );
};
