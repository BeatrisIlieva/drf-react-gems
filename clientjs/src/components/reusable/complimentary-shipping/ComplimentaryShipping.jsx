import { TruckIcon } from '../../reusable/truck-icon/TruckIncon';

import styles from './ComplimentaryShipping.module.css';

export const ComplimentaryShipping = () => {
    return (
        <button className={styles['complimentary-shipping']}>
            <TruckIcon />
            <span>Complimentary 2-day shipping</span>
        </button>
    );
};
