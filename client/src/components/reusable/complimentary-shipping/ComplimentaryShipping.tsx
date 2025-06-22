import type { ReactElement } from 'react';
import { TruckIcon } from '../truck-icon/TruckIncon';

import styles from './ComplimentaryShipping.module.scss';

export const ComplimentaryShipping = (): ReactElement => {
    return (
        <button className={styles['complimentary-shipping']}>
            <TruckIcon />
            <span>Complimentary 2-day shipping</span>
        </button>
    );
};
