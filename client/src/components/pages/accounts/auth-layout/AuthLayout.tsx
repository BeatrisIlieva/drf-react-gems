import React from 'react';
import type { ReactNode } from 'react';
import styles from './AuthLayout.module.scss';

interface AuthLayoutProps {
    children: ReactNode;
}

export const AuthLayout: React.FC<AuthLayoutProps> = ({
    children
}) => {
    return (
        <section className={styles['auth-layout']}>
            <div className={styles['thumbnail']}>
                <img
                    src='https://res.cloudinary.com/dpgvbozrb/image/upload/v1747296590/37_nfvprf.avif'
                    alt='necklace-image'
                />
            </div>
            <div className={styles['form']}>{children}</div>
        </section>
    );
};
