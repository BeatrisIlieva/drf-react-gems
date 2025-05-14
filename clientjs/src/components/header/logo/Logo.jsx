import { Link } from 'react-router';

import styles from './Logo.module.css';

export const Logo = () => {
    return (
        <Link to='/' className={styles['logo']}>
            <h1>DRF-React-TS Gems</h1>
        </Link>
    );
};
