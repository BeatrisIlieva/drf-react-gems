import styles from './ShadowBox.module.scss';

export const ShadowBox = ({ children, title = null }) => {
    return (
        <section className={styles['shadow-box']}>
            {title && <h3>{title}</h3>}

            {children}
        </section>
    );
};
