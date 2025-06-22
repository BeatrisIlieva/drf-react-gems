import type { ReactElement } from 'react';
import styles from './RelatedProducts.module.scss';
import { Link } from 'react-router';
import { useCategoryName } from '../../../../../../hooks/products/useCategoryName';
import type { Props } from './types';

export const RelatedProducts = ({
    relatedProducts,
    collectionName,
    productId
}: Props): ReactElement => {
    const { categoryNameCapitalizedPlural } = useCategoryName();
    return (
        <ul className={styles['related-products']}>
            {relatedProducts.map((product) => (
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
