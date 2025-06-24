import type { ReactElement } from 'react';
import styles from './Items.module.scss';
import { ProductCard } from '../product-card/ProductCard';
import { useProductListContext } from '../../../../contexts/ProductListContext';

export const Items = (): ReactElement => {
    const { products, loading } = useProductListContext();
    return (
        <ul className={styles['products']}>
            {products?.map((product) => (
                <ProductCard key={product.id} {...product} />
            ))}

            {loading && products.length > 0 && (
                <div className={styles['loading-more']}>
                    <div
                        className={styles['loading-spinner']}
                    ></div>
                    <p>Loading more products...</p>
                </div>
            )}
        </ul>
    );
};
