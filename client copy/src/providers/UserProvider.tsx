import type { ReactNode } from 'react';
import { UserContext } from '../contexts/UserContext';
import { usePersistedState } from '../hooks/usePersistedState';
import { useGuest } from '../hooks/useGuest';
import type { UserContextPayload } from '../types/UserContext';

interface Props {
    children: ReactNode;
}

export const UserProvider = ({ children }: Props) => {
    const [authData, setAuthData] = usePersistedState<UserContextPayload>(
        'auth',
        {
            _id: '',
            email: '',
            refresh: '',
            access: ''
        }
    );

    const { clearGuestData } = useGuest();

    const userLoginHandler = (resultData: UserContextPayload) => {
        setAuthData(resultData);
    };

    const userLogoutHandler = () => {
        setAuthData({
            _id: '',
            email: '',
            refresh: '',
            access: ''
        });
        clearGuestData();
    };

    return (
        <UserContext.Provider
            value={{ ...authData, userLoginHandler, userLogoutHandler }}
        >
            {children}
        </UserContext.Provider>
    );
};
