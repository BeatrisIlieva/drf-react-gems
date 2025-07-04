import { useState, useEffect } from 'react';
import { Icon } from '../icon/Icon';
import styles from './Button.module.scss';

export const Button = ({
    title,
    callbackHandler,
    color,
    actionType = 'button',
    pending = false,
    success = false,
    disabled = false,
    buttonGrow = '0',
    width = 'auto'
}) => {
    const [showSuccess, setShowSuccess] = useState(false);

    useEffect(() => {
        if (success && !pending) {
            setShowSuccess(true);
            const timer = setTimeout(() => {
                setShowSuccess(false);
            }, 2000);

            return () => clearTimeout(timer);
        }
    }, [success, pending]);

    const handleClick = () => {
        if (actionType === 'submit') {
            if (
                callbackHandler &&
                callbackHandler.toString() !== '() => {}'
            ) {
                callbackHandler();
            }
        } else {
            callbackHandler();
        }
    };

    const getButtonContent = () => {
        if (pending) {
            return (
                <span className={styles['button-content']} key="pending">
                    <Icon name='ellipsis' fontSize={1.2} />
                </span>
            );
        } else if (showSuccess) {
            return (
                <span className={styles['button-content']} key="success">
                    <Icon name='check' fontSize={1.2} />
                </span>
            );
        } else {
            return (
                <span className={styles['button-content']} key="title">
                    {title}
                </span>
            );
        }
    };

    return (
        <button
            onClick={handleClick}
            className={`${styles['btn']} ${styles[color]} ${
                pending ? styles['pending'] : ''
            } ${showSuccess ? styles['success'] : ''}`}
            type={actionType}
            disabled={disabled || pending}
            style={{ flexGrow: buttonGrow, width: width !== 'auto' ? `${width}em` : 'auto' }}
        >
            <div className={styles['content-wrapper']}>
                {getButtonContent()}
            </div>
        </button>
    );
};
