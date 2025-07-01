import { Icon } from '../icon/Icon';

import styles from './ChevronToggle.module.scss';

export const ChevronToggle = ({ onToggle, isOpen }) => {
    return (
        <span
            onClick={onToggle}
            className={`${styles['toggle-icon']} ${
                isOpen ? styles['rotated'] : ''
            }`}
        >
            <Icon
                name={isOpen ? 'arrowUp' : 'arrowDown'}
                isSubtle={true}
                fontSize={0.6}
            />
        </span>
    );
};
