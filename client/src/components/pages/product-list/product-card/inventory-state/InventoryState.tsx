import type { ReactElement } from 'react';

import styles from './InventoryState.module.scss';

interface Props {
    positive: boolean;
    label: string;
}

export const InventoryState = ({
    positive,
    label
}: Props): ReactElement => {
    return (
        <div className={styles['inventory-state']}>
            <span
                className={
                    positive === false
                        ? `${styles['on']}`
                        : `${styles['off']}`
                }
            ></span>
            <span>{label}</span>
        </div>
    );
};
