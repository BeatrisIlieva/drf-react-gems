import { useState, type ReactElement } from 'react';
import type { Product } from '../../../../types/ProductList';
import styles from './ProductCard.module.scss';
import { Icon } from '../../../reusable/icon/Icon';
import { ToggleImageButtons } from './toggle-image-buttons/ToggleImageButtons';
import { InventoryState } from './inventory-state/InventoryState';

export const ProductCard = ({
    id,
    collectionName,
    firstImage,
    secondImage,
    isSoldOut,
    min,
    max
}: Product): ReactElement => {
    const [selectedImageIndex, setSelectedImageIndex] = useState(0);

    return (
        <article className={styles['product-card']}>
            <Icon name={'heart'} />

            <div className={styles['thumbnail']}>
                <img
                    src={
                        selectedImageIndex === 0
                            ? firstImage
                            : secondImage
                    }
                    alt={collectionName}
                />
            </div>

            <footer>
                <InventoryState
                    positive={isSoldOut}
                    label={isSoldOut ? 'Sold Out' : 'In Stock'}
                />
                <ToggleImageButtons
                    selectedIndex={selectedImageIndex}
                    onSelect={setSelectedImageIndex}
                />
            </footer>
        </article>
    );
};
