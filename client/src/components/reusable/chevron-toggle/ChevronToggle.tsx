import type { ReactElement } from 'react';

import { Icon } from '../icon/Icon';

import styles from './ChevronToggle.module.scss';

interface Props {
    isOpen: boolean;
    onToggle: () => void;
}

export const ChevronToggle = ({
    onToggle,
    isOpen
}: Props): ReactElement => {
    return (
        <span
            onClick={onToggle}
            className={`${styles['toggle-icon']} ${isOpen ? styles['rotated'] : ''}`}
        >
            <Icon
                name={isOpen ? 'arrowUp' : 'arrowDown'}
                isSubtle={true}
                fontSize={0.6}
            />
        </span>
    );
};
