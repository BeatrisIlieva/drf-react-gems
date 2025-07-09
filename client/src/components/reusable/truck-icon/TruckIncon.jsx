import { faTruckFast } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import styles from './TruckIcon.module.scss';

export const TruckIcon = () => {
    return <FontAwesomeIcon icon={faTruckFast} className={styles['truck-icon']} />;
};
