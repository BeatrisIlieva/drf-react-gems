import styles from './ProductItems.module.scss';

import { ProductCard } from './product-card/ProductCard';

export const ProductItems = ({ products }) => {

    return (
        <ul className={styles['products']}>
            {products?.map((product) => (
                <ProductCard key={product.id} {...product} />
            ))}
        </ul>
    );
};
