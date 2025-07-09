import { useGuest } from '../hooks/useGuest';
import usePersistedState from '../hooks/usePersistedState';

import { UserContext } from '../contexts/UserContext';

export const UserProvider = ({ children }) => {
    const [authData, setAuthData] = usePersistedState('auth', {});
    const { clearGuestData } = useGuest();

    const userLoginHandler = resultData => {
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
                userLogoutHandler,
            }}
        >
            {children}
        </UserContext.Provider>
    );
};
