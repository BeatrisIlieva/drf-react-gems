import { UserAction } from '../../../reusable/user-action/UserAction';
import { ProductDetails } from './product-details/ProductDetails';

import styles from './MainContent.module.scss';

export const MainContent = () => {
    return (
        <section className={styles['main-content']}>
            <ProductDetails />
            <UserAction />
        </section>
    );
};
