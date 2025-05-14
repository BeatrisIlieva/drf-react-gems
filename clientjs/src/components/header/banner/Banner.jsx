import styles from './Banner.module.css';

export const Banner = () => {
    return (
        <div className={styles['banner']}>
            <p>Complimentary two-day shipping</p>
            <button>Learn More</button>
        </div>
    );
};
