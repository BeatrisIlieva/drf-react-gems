import type { ReactElement } from 'react';

import { icons } from './icons';

import styles from './Icon.module.css';

type IconName = keyof typeof icons;

type Props = {
    name: IconName;
    width?: number;
    isSubtle?: boolean;
};

export const Icon = ({ name, width, isSubtle }: Props): ReactElement => {
    return (
        <span
            className={styles['icon']}
            style={{
                fontSize: width ? `${width}em` : `${1.1}em`,
                opacity: isSubtle ? 0.6 : 1
            }}
        >
            {icons[name]}
        </span>
    );
};
