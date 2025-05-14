import { useContext } from 'react';
import useUserContext, { UserContext } from '../../../contexts/UserContext';
import { useLogout } from '../../../api/authApi';

export const Logout = () => {
    const { refresh, access } = useContext(UserContext);
    const { logout } = useLogout();

    const { userLogoutHandler } = useUserContext();

    const logoutHandler = async () => {
        const data = { refresh, access };

        try {
            await logout(data);

            userLogoutHandler();
        } catch (err) {
            console.log(err.message);
        }
    };

    return <button onClick={logoutHandler}>Sign out</button>;
};
