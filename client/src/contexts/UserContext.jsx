import { createContext, useContext } from 'react';

export const UserContext = createContext({
    id: '',
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
