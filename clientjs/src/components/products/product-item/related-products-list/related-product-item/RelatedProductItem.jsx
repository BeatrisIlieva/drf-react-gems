import { useProductItemContext } from '../../../../../contexts/ProductItemContext';

import styles from './RelatedProductItem.module.css';

export const RelatedProductItem = ({ item }) => {
    const { product, productCategory } = useProductItemContext();

    return (
        <li
            key={item.id}
            className={`${styles['thumbnail']} ${
                product.id === item.id ? styles['selected'] : ''
            }`.trim()}
        >
            <img src={item.first_image} alt={productCategory} />
        </li>
    );
};
