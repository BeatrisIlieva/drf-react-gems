import { MaterialsInfo } from './materials-info/MaterialsInfo';
import styles from './ProductCard.module.css';


export const ProductCard = ({
    id,
    first_image,
    collection__name,
    reference__name,
    category__name,
    stones,
    materials_count,
    min_price,
    max_price
}) => {
    return (
        <li className={styles['product-card']}>
            <span className={styles['wrapper-top']}>
                <span className={styles['thumbnail']}>
                    <img
                        src={first_image}
                        alt={`${collection__name} ${reference__name} ${category__name}`}
                    />
                </span>
                <MaterialsInfo
                    id={id}
                    stones={stones}
                    materials_count={materials_count}
                />
            </span>
            <span className={styles['wrapper-bottom']}>
                <span>{`${collection__name} ${reference__name} ${category__name}`}</span>
                <span>{`$${min_price} - $${max_price}`}</span>
            </span>
        </li>
    );
};
