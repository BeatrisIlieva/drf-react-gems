import type { ReactElement } from 'react';
import styles from './Button.module.scss';

interface Props {
    title: string;
    callbackHandler: () => void;
    color: string;
    actionType?: 'button' | 'submit' | 'reset';
    pending?: boolean;
    disabled?: boolean;
}

export const Button = ({
    title,
    callbackHandler,
    color,
    actionType = 'button',
    pending = false,
    disabled = false
}: Props): ReactElement => {
    return (
        <button
            onClick={callbackHandler}
            className={`${styles['btn']} ${styles[color]}`}
            type={actionType}
            disabled={disabled}
        >
            {pending ? 'pending...' : title}
        </button>
    );
};
