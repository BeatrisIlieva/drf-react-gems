import { createContext, useContext } from 'react';
import type { UserContextType } from '../types/User';

export const UserContext = createContext<UserContextType>({
    id: '',
    email: '',
    refresh: '',
    access: '',
    userLoginHandler: () => null,
    userLogoutHandler: () => null,
});

export default function useUserContext(): UserContextType {
    const data = useContext(UserContext);
    return data;
}
