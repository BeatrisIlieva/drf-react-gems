import { ProductCard } from './product-card/ProductCard';

import styles from './ProductItems.module.scss';

export const ProductItems = ({ products, onMoveToBag }) => {
    return (
        <ul className={styles['products']}>
            {products?.map(product => (
                <ProductCard key={`${product.id}-${product.collectionName}-${product.colorName}`} {...product} onMoveToBag={onMoveToBag} />
            ))}
        </ul>
    );
};
