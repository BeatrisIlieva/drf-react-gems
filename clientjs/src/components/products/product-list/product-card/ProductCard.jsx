import { useState } from 'react';

import { HeartIcon } from '../../../reusable/heart-icon/HeartIcon';
import { DotIcon } from './dot-icon/DotIcon';
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
    const [firstImageIsSelected, setFirstImageIsSelected] = useState(true);

    const toggleFirstImageIsSelectedHandler = () => {
        setFirstImageIsSelected(() => !firstImageIsSelected);
    };

    return (
        <li className={styles['product-card']}>
            <span className={styles['user-action']}>
                <HeartIcon />
            </span>

            <span className={styles['wrapper-top']}>
                <span className={styles['thumbnail']}>
                    <img
                        src={first_image}
                        alt={`${collection__name} ${reference__name} ${category__name}`}
                    />
                </span>
                <span className={styles['switch-image']}>
                    <DotIcon
                        toggleHandler={toggleFirstImageIsSelectedHandler}
                        disabled={firstImageIsSelected}
                    />
                    <DotIcon
                        toggleHandler={toggleFirstImageIsSelectedHandler}
                        disabled={!firstImageIsSelected}
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
