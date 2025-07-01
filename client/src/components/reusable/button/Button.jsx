import styles from './Button.module.scss';

export const Button = ({
    title,
    callbackHandler,
    color,
    actionType = 'button',
    pending = false,
    disabled = false
}) => {
    const handleClick = () => {
        // For submit buttons, let the form handle submission naturally
        if (actionType === 'submit') {
            // Don't prevent default - let the form action handle it
            // Only call callback if it's not an empty function
            if (
                callbackHandler &&
                callbackHandler.toString() !== '() => {}'
            ) {
                callbackHandler();
            }
        } else {
            // For non-submit buttons, call the callback
            callbackHandler();
        }
    };

    return (
        <button
            onClick={handleClick}
            className={`${styles['btn']} ${styles[color]}`}
            type={actionType}
            disabled={disabled || pending}
        >
            {pending ? 'pending...' : title}
        </button>
    );
};
