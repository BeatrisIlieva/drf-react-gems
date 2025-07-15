import { Link } from 'react-router';

import { useCategoryName } from '../../../../hooks/useCategoryName';

import { useProductItemContext } from '../../../../contexts/ProductItemContext';

import styles from './RelatedProducts.module.scss';

export const RelatedProducts = () => {
    const { categoryNameCapitalizedPlural, categoryName } = useCategoryName();
    const { relatedCollectionProducts, productId, collectionName } = useProductItemContext();

    const products = Array.isArray(relatedCollectionProducts) ? relatedCollectionProducts : [];

    return (
        <ul className={styles['related-products']}>
            {products.map(product => (
                <li key={product.id} className={product.id === productId ? styles['selected'] : ''}>
                    <Link to={`/products/${categoryName}/${product.id}`}>
                        <img
                            src={product.firstImage}
                            alt={`${collectionName} ${categoryNameCapitalizedPlural}`}
                        />
                    </Link>
                </li>
            ))}
        </ul>
    );
};
