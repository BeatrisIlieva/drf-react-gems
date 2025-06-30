import type { ReactElement, ReactNode } from 'react';
import styles from './DetailsContainer.module.scss';

interface DetailsContainerProps {
    children: ReactNode;
}

export const DetailsContainer = ({
    children
}: DetailsContainerProps): ReactElement => {
    return (
        <section className={styles['details-container']}>
            {children}
        </section>
    );
};
