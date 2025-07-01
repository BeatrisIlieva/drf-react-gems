import styles from './DetailsContainer.module.scss';

export const DetailsContainer = ({ children }) => {
    return (
        <section className={styles['details-container']}>
            {children}
        </section>
    );
};
