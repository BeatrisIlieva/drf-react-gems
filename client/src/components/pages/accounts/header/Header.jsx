import styles from './Header.module.scss';

export const Header = () => {
    return (
        <header className={styles['accounts-header']}>
            <div className={styles['overlay']}></div>
            <h3>Welcome Back</h3>
            <div className={styles['thumbnail']}>
                <img
                    src='https://res.cloudinary.com/dpgvbozrb/image/upload/v1745748165/top_mrzjd0.webp'
                    alt='welcome-image'
                />
            </div>
        </header>
    );
};
