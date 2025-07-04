import { Link } from 'react-router';

import styles from './Logo.module.scss';

export const Logo = () => {
    return (
        <Link to='/' className={styles['logo']}>
            <span>DRF React Gems</span>
        </Link>
    );
};
