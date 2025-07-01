import { ShopByCategory } from '../../common/shop-by-category/ShopByCategory';

import styles from './EmptyList.module.scss';

export const EmptyList = ({ title }) => {
    return (
        <div className={styles['empty-bag-container']}>
            <div className={styles['empty-bag-message']}>
                <h3>Your {title} is empty</h3>
                <p>
                    Browse our categories below to discover
                    beautiful pieces for your collection
                </p>
            </div>
            <ShopByCategory />
        </div>
    );
};
