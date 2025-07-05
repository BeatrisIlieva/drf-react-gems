import { ProductSummaryItem } from './product-summary-item/ProductSummaryItem';
import styles from './ProductsSummaryList.module.scss';
import { Children } from 'react';

export const ProductsSummaryList = ({ children, products, position = 'top' }) => {    
    return (
        <section className={styles['products-summary-list']}>
            {position === 'top' && children}
            <ul
                className={styles['products-summary-list']}
                style={{
                    gridTemplateRows: `repeat(${products.length}, 1fr)`
                }}
            >
                {products.map((item) => (
                    <div className={styles['wrapper']} key={item.id}>
                        <ProductSummaryItem {...item} />
                        {position === 'bottom' && children}
                    </div>
                ))}
            </ul>
        </section>
    );
};
