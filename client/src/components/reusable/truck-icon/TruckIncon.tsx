import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTruckFast } from '@fortawesome/free-solid-svg-icons';

import styles from './TruckIcon.module.scss';
import type { ReactElement } from 'react';

export const TruckIcon = (): ReactElement => {
    return (
        <FontAwesomeIcon
            icon={faTruckFast}
            className={styles['truck-icon']}
        />
    );
};
