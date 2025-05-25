import { useState } from 'react';

import { HeartIcon } from '../../../reusable/heart-icon/HeartIcon';
import { DotIcon } from './dot-icon/DotIcon';
import { MaterialsInfo } from './materials-info/MaterialsInfo';
import styles from './ProductCard.module.css';
import { faCircle } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

export const ProductCard = ({
    id,
    first_image,
    second_image,
    collection__name,
    reference__name,
    category__name,
    stones,
    materials_count,
    price,
    is_sold_out
}) => {
    const [firstImageIsSelected, setFirstImageIsSelected] = useState(true);

    const toggleFirstImageIsSelectedHandler = () => {
        setFirstImageIsSelected(() => !firstImageIsSelected);
    };

    ''.charAt(0).toUpperCase() + ''.slice(1);

    const categoryName = category__name.charAt(0).toUpperCase() + category__name.slice(1);

    return (
        <li className={styles['product-card']}>
            <span className={styles['user-action']}>
                <span className={styles['sold-out']}>
                    <FontAwesomeIcon
                        icon={faCircle}
                        style={{ color: is_sold_out ? '#d82325' : '#208402' }}
                    />
                    <span>{is_sold_out ? 'Sold Out' : 'In Stock'}</span>
                </span>
                <HeartIcon />
            </span>

            <span className={styles['wrapper-top']}>
                <span className={styles['thumbnail']}>
                    <img
                        src={firstImageIsSelected ? first_image : second_image}
                        alt={`${collection__name} ${reference__name} ${categoryName}`}
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
                <MaterialsInfo id={id} stones={stones} materials_count={materials_count} />
            </span>
            <span className={styles['wrapper-bottom']}>
                <span>{`${collection__name} ${reference__name} ${categoryName}`}</span>
                <span>{`$${price}`}</span>
            </span>
        </li>
    );
};
