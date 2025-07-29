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
        localStorage.setItem('migratedShoppingBag', false);
        localStorage.setItem('migratedWishlist', false);

        localStorage.setItem('shopping-bag-items', []);
        localStorage.setItem('shopping-bag-total-price', 0);
        localStorage.setItem('shopping-bag-count', 0);

        localStorage.setItem('wishlist-items', []);
        localStorage.setItem('wishlist-count', 0);
    }, [setAuthData]);

    const contextValue = useMemo(
        () => ({
            ...authData,
            userLoginHandler,
            userLogoutHandler,
            setAuthData,
        }),
        [authData, userLoginHandler, userLogoutHandler, setAuthData]
    );

    return <UserContext.Provider value={contextValue}>{children}</UserContext.Provider>;
};
