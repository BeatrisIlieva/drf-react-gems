import { icons } from './icons';

import styles from './Icon.module.scss';

export const Icon = ({ name, fontSize, isSubtle, callbackHandler = null }) => {
    return (
        <span
            onClick={callbackHandler}
            className={styles['icon']}
            style={{
                fontSize: fontSize ? `${fontSize}em` : `${1.1}em`,
                opacity: isSubtle ? 0.6 : 1,
            }}
        >
            {icons[name]}
        </span>
    );
};
