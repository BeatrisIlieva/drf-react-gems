import styles from './Button.module.css';

export const Button = ({
    title,
    callbackHandler,
    color,
    actionType,
    pending
}) => {
    return (
        <button
            onClick={callbackHandler}
            className={`${styles['btn']} ${styles[color]}`}
            type={actionType}
        >
            {pending ? 'pending...' : title}
        </button>
    );
};
