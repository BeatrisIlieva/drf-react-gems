import { ComplimentaryShipping } from '../../../reusable/complimentary-shipping/ComplimentaryShipping';

import styles from './Banner.module.scss';

export const Banner = () => {
    return (
        <div className={styles['banner']}>
            <ComplimentaryShipping />
        </div>
    );
};
