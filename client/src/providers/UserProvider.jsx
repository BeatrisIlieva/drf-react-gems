import { useCallback, useMemo } from 'react';

import usePersistedState from '../hooks/usePersistedState';

import { UserContext } from '../contexts/UserContext';

export const UserProvider = ({ children }) => {
    const [authData, setAuthData] = usePersistedState('auth', {});

    const userLoginHandler = useCallback(
        resultData => {
            setAuthData(resultData);
        },
        [setAuthData]
    );

    const userLogoutHandler = useCallback(() => {
        setAuthData({});
    }, [setAuthData]);

    const contextValue = useMemo(
        () => ({
            ...authData,
            userLoginHandler,
            userLogoutHandler,
        }),
        [authData, userLoginHandler, userLogoutHandler]
    );

    return <UserContext.Provider value={contextValue}>{children}</UserContext.Provider>;
};
