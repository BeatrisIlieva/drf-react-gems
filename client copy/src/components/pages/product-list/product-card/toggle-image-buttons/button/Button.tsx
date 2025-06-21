import type { ReactElement } from 'react';

import styles from './Button.module.scss';

interface Props {
    onClick: () => void;
    isSelected: boolean;
}

export const Button = ({
    onClick,
    isSelected
}: Props): ReactElement => {
    return (
        <button
            onClick={onClick}
            className={styles['button']}
            disabled={isSelected}
        ></button>
    );
};
