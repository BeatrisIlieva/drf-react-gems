import React from 'react';
import useUserContext from '../../../../contexts/UserContext';
import { useLogout } from '../../../../api/authApi';

export const Logout: React.FC = () => {
    const { logout } = useLogout();
    const { userLogoutHandler } = useUserContext();

    const logoutHandler = async () => {
        try {
            await logout();
            userLogoutHandler();
        } catch (err) {
            console.log(err instanceof Error ? err.message : String(err));
        }
    };

    return <button onClick={logoutHandler}>Sign out</button>;
};
