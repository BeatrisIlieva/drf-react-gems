import { useEffect, useState, type ReactElement } from 'react';
import type { Product } from '../../../../types/ProductList';
import styles from './ProductCard.module.scss';
import { Icon } from '../../../reusable/icon/Icon';
import { ToggleImageButtons } from './toggle-image-buttons/ToggleImageButtons';
import { InventoryState } from './inventory-state/InventoryState';
import { useCategoryName } from '../../../../hooks/useCategoryName';
import { StyledTextBlock } from '../../../reusable/styled-text-block/StyledTextBlock';
import { formatPrice } from '../../../../utils/formatPrice';

export const ProductCard = ({
    id,
    collectionName,
    firstImage,
    secondImage,
    isSoldOut,
    colorName,
    stoneName,
    metalName,
    min,
    max
}: Product): ReactElement => {
    const [selectedImageIndex, setSelectedImageIndex] = useState(0);
    const { categoryNameCapitalizedSingular, categoryName } =
        useCategoryName();
    const formattedMin = formatPrice(min);
    const formattedMax = formatPrice(max);

    useEffect(() => {
        setSelectedImageIndex(0);
    }, [categoryName]);

    return (
        <article className={styles['product-card']}>
            <div className={styles['wrapper']}>
                <Icon name={'heart'} />

                <div className={styles['thumbnail']}>
                    <img
                        src={
                            selectedImageIndex === 0
                                ? firstImage
                                : secondImage
                        }
                        className={`${selectedImageIndex === 0 ? styles['slide-in-right'] : styles['slide-in-left']}`}
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
            </div>
            <div className={styles['product-info']}>
                <StyledTextBlock
                    text={`${collectionName} ${categoryNameCapitalizedSingular}`}
                />
                <StyledTextBlock
                    text={`${formattedMin} - ${formattedMax}`}
                    isLighter={true}
                />
                <StyledTextBlock
                    text={`${colorName} ${stoneName} set in ${metalName}`}
                    isSubtle={true}
                />
            </div>
        </article>
    );
};
