import { createContext, useContext } from 'react';

export const UserContext = createContext({
    _id: '',
    email: '',
    refresh: '',
    access: '',
    userLoginHandler: () => null,
    userLogoutHandler: () => null,
});

export default function useUserContext() {
    const data = useContext(UserContext);

    return data;
}
