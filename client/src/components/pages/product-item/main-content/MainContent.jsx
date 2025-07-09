import { ProductDetails } from './product-details/ProductDetails';
import { UserAction } from './user-action/UserAction';

import styles from './MainContent.module.scss';

export const MainContent = () => {
    return (
        <section className={styles['main-content']}>
            <ProductDetails />
            <UserAction />
        </section>
    );
};
