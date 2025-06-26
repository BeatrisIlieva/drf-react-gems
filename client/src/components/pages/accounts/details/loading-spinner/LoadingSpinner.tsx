import React from 'react';
import styles from './LoadingSpinner.module.scss';

interface Props {
    size?: 'small' | 'medium' | 'large';
    message?: string;
}

export const LoadingSpinner: React.FC<Props> = ({ 
    size = 'medium', 
    message = 'Loading...' 
}) => {
    return (
        <div className={styles['loading-container']}>
            <div className={`${styles['spinner']} ${styles[size]}`} />
            {message && <p className={styles['loading-text']}>{message}</p>}
        </div>
    );
};
