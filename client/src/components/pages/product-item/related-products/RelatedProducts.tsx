import type { ReactElement } from 'react';

import styles from './RelatedProducts.module.scss';
import { useProductItemContext } from '../../../../contexts/ProductItemContext';

export const RelatedProducts = (): ReactElement => {
    const { relatedProducts } = useProductItemContext();

    return (
        <section className={styles['related-products']}>
            <h4>You may also like</h4>
            <ul>
                {relatedProducts!.map((product) => (
                    <li
                        key={product.id}
                        className={styles['related-product']}
                    >
                        <img
                            src={product.firstImage}
                            alt={`Related product ${product.id}`}
                        />
                        {/* <p>{product.productType}</p> */}
                    </li>
                ))}
            </ul>
        </section>
    );
};
