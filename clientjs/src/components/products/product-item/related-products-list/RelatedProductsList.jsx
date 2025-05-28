import { useProductItemContext } from '../../../../contexts/ProductItemContext';
import { RelatedProductItem } from './related-product-item/RelatedProductItem';

import styles from './RelatedProductsList.module.css';

export const RelatedProductsList = () => {
    const { product } = useProductItemContext();

    return (
        <ul className={styles['related-products']}>
            {product.related_products.map((item) => (
                <RelatedProductItem key={item.id} item={item} />
            ))}
        </ul>
    );
};
