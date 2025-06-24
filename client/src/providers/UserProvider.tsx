
import type { ReactNode } from 'react';
import { UserContext } from '../contexts/UserContext';
import usePersistedState from '../hooks/usePersistedState';

import type { UserData } from '../types/User';
import { useGuest } from '../hooks/useGuest';

interface UserProviderProps {
    children: ReactNode;
}

export default function UserProvider({ children }: UserProviderProps) {
    const [authData, setAuthData] = usePersistedState<UserData>('auth', {});
    const { clearGuestData } = useGuest();

    const userLoginHandler = (resultData: UserData) => {
        setAuthData(resultData);
    };

    const userLogoutHandler = () => {
        setAuthData({});
        clearGuestData();
    };

    return (
        <UserContext.Provider
            value={{ ...authData, userLoginHandler, userLogoutHandler }}
        >
            {children}
        </UserContext.Provider>
    );
}
