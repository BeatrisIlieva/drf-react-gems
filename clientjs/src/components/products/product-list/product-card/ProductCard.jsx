import styles from './ProductCard.module.css';
import { StoneImage } from './stone-image/StoneImage';

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
                <span className={styles['materials-info']}>
                    <span className={styles['stones']}>
                        {stones.map((item) =>
                            id === Number(item.product_id) ? (
                                <span className={styles['selected-stone']}>
                                    <StoneImage
                                        key={`${id}-${item.color}-${item.name}`}
                                        {...item}
                                    />
                                </span>
                            ) : (
                                <StoneImage
                                    key={`${id}-${item.color}-${item.name}`}
                                    {...item}
                                />
                            )
                        )}
                    </span>
                    <span className={styles['materials']}>
                        <span>{materials_count}</span>
                        <span>{materials_count > 1 ? 'metals' : 'metal'}</span>
                    </span>
                </span>
            </span>
            <span className={styles['wrapper-bottom']}>
                <span>{`${collection__name} ${reference__name} ${category__name}`}</span>
                <span>{`$${min_price} - $${max_price}`}</span>
            </span>
        </li>
    );
};
