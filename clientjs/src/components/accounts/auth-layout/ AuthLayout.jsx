import styles from './AuthLayout.module.css';

export const AuthLayout = ({ children }) => {
    return (
        <section className={styles['auth-layout']}>
            <div className={styles['thumbnail']}>
                <img src='https://res.cloudinary.com/dpgvbozrb/image/upload/v1747296590/37_nfvprf.avif' alt='necklace-image' />
            </div>
            <div className={styles['form']}>{children}</div>
        </section>
    );
};
