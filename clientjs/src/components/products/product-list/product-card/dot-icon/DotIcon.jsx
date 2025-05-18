import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCircle } from '@fortawesome/free-solid-svg-icons';

import styles from './DotIcon.module.css';

export const DotIcon = ({ toggleHandler, disabled}) => {
    const className = [
        styles['dot-icon'],          
        disabled ? styles['disabled'] : ''
    ].join(' ').trim();

    return (
        <button onClick={toggleHandler} disabled={disabled}>
            <FontAwesomeIcon
                icon={faCircle}
                className={className}
            />
        </button>
    );
};
