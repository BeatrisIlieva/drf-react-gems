import type { ReactElement } from 'react';
import { Link } from 'react-router';

import styles from './Logo.module.scss';

export const Logo = (): ReactElement => {
    return (
        <Link to='/' className={styles['logo']}>
            <span>DRF React TS Gems</span>
        </Link>
    );
};
