import type { ReactElement } from 'react';
import styles from './RelatedProducts.module.scss';
import { Link } from 'react-router';
import { useCategoryName } from '../../../../../../hooks/products/useCategoryName';
import { useProductItemContext } from '../../../../../../contexts/ProductItemContext';

export const RelatedProducts = (): ReactElement => {
    const { categoryNameCapitalizedPlural } = useCategoryName();
    const {
        relatedCollectionProducts,
        productId,
        collectionName
    } = useProductItemContext();

    return (
        <ul className={styles['related-products']}>
            {relatedCollectionProducts!.map((product) => (
                <li
                    key={product.id}
                    className={
                        product.id === productId
                            ? styles['selected']
                            : ''
                    }
                >
                    <Link
                        to={`/products/${categoryNameCapitalizedPlural}/${product.id}`}
                    >
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
