import { createContext, useContext } from 'react';
import type { UserContextType } from '../types/UserContext';

export const UserContext = createContext<UserContextType>({
    _id: '',
    email: '',
    refresh: '',
    access: '',
    userLoginHandler: () => null,
    userLogoutHandler: () => null
});

export const useUserContext = () => {
    const data = useContext(UserContext);

    return data;
};
