import styles from './DetailsContainer.module.scss';

export const DetailsContainer = ({ children, title }) => {
    return (
        <section className={styles['details-container']}>
            <h3>{title}</h3>
            {children}
        </section>
    );
};
