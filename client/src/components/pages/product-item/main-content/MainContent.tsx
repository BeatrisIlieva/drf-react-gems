import type { ReactElement } from 'react';
import styles from './MainContent.module.scss';
import { ProductDetails } from './product-details/ProductDetails';
import { UserAction } from './user-action/UserAction';

export const MainContent = (): ReactElement => {
    return (
        <section className={styles['main-content']}>
            <ProductDetails />
            <UserAction />
        </section>
    );
};
