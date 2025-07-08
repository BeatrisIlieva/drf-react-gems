import styles from './LoadingSpinner.module.scss';

export const LoadingSpinner = ({ fullHeight = false, minHeight = "40vh" }) => {
    const overlayClass = fullHeight 
        ? `${styles['overlay']} ${styles['full-height']}` 
        : styles['overlay'];
    
    const overlayStyle = !fullHeight ? { minHeight } : {};

    return (
        <div className={overlayClass} style={overlayStyle}>
            <div className={styles['loading-spinner']}>
                <div className={styles['thumbnail']}>
                    <img
                        src='https://res.cloudinary.com/deztgvefu/image/upload/v1706426486/template_images/cute-little-pink-cat-watercolor-png_2_kxmwtq.webp'
                        alt='loading'
                    />
                </div>
                <p>Loading...</p>
            </div>
        </div>
    );
};
