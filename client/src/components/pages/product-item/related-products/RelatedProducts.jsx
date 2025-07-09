import { Link } from 'react-router';

import { useProductItemContext } from '../../../../contexts/ProductItemContext';

import styles from './RelatedProducts.module.scss';

export const RelatedProducts = () => {
    const { relatedProducts } = useProductItemContext();

    return (
        <section className={styles['related-products']}>
            <h4>You may also like</h4>
            <ul>
                {relatedProducts.map(product => (
                    <li key={product.id} className={styles['related-product']}>
                        <Link to={`/products/${product.productType}/${product.id}`}>
                            <img src={product.firstImage} alt={`Related product ${product.id}`} />
                        </Link>
                    </li>
                ))}
            </ul>
        </section>
    );
};
