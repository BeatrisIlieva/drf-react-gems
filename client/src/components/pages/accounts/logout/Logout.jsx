import { Icon } from '../../../reusable/icon/Icon';

import { useAuthentication } from '../../../../api/authApi';

import { useUserContext } from '../../../../contexts/UserContext';

import styles from './Logout.module.scss';

export const Logout = () => {
    const { logout } = useAuthentication();
    const { userLogoutHandler } = useUserContext();

    const logoutHandler = async () => {
        try {
            await logout();
            
            userLogoutHandler();
        } catch (err) {
            console.error(err instanceof Error ? err.message : String(err));
        }
    };

    return (
        <button onClick={logoutHandler} className={styles['sign-out']}>
            <Icon name="sign-out" fontSize={0.75} isSubtle={true} />
            <span>Sign Out</span>
        </button>
    );
};
