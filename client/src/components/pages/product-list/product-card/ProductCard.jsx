import { useCallback, useEffect, useState } from 'react';
import styles from './ProductCard.module.scss';
import { Icon } from '../../../reusable/icon/Icon';
import { ToggleImageButtons } from './toggle-image-buttons/ToggleImageButtons';
import { InventoryState } from './inventory-state/InventoryState';
import { useCategoryName } from '../../../../hooks/products/useCategoryName';
import { StyledTextBlock } from '../../../reusable/styled-text-block/StyledTextBlock';
import { formatPrice } from '../../../../utils/formatPrice';
import { Stars } from '../../../reusable/stars/Stars';
import { useNavigate } from 'react-router';
import { useWishlistContext } from '../../../../contexts/WishlistContext';

export const ProductCard = ({
    id,
    collectionName,
    firstImage,
    secondImage,
    isSoldOut,
    colorName,
    stoneName,
    metalName,
    minPrice,
    maxPrice,
    averageRating
}) => {
    const [selectedImageIndex, setSelectedImageIndex] =
        useState(0);
    const { categoryNameCapitalizedSingular, categoryName } =
        useCategoryName();
    const formattedMinPrice = formatPrice(minPrice);
    const formattedMaxPrice = formatPrice(maxPrice);
    const navigate = useNavigate();
    const { addToWishlist, removeFromWishlist, isInWishlist } =
        useWishlistContext();

    const handleWishlistToggle = useCallback(async () => {
        const category = categoryName?.slice(
            0,
            categoryName?.length - 1
        );

        if (category && id) {
            if (isInWishlist(category, id)) {
                await removeFromWishlist(category, id);
            } else {
                await addToWishlist(category, id);
            }
        }
    }, [
        addToWishlist,
        removeFromWishlist,
        isInWishlist,
        categoryName,
        id
    ]);

    const category = categoryName?.slice(
        0,
        categoryName?.length - 1
    );
    const isItemInWishlist =
        category && id ? isInWishlist(category, id) : false;

    const navigateToProductItem = useCallback(() => {
        navigate(`/products/${categoryName}/${id}`);
    }, [categoryName, id, navigate]);

    useEffect(() => {
        setSelectedImageIndex(0);
    }, [categoryName]);

    return (
        <article className={styles['product-card']}>
            <div className={styles['wrapper']}>
                <button
                    onClick={handleWishlistToggle}
                    className={styles['wishlist-button']}
                    aria-label={
                        isItemInWishlist
                            ? 'Remove from wishlist'
                            : 'Add to wishlist'
                    }
                >
                    <Icon
                        name={
                            isItemInWishlist
                                ? 'heart-filled'
                                : 'heart'
                        }
                    />
                </button>

                <div className={styles['thumbnail']}>
                    <img
                        src={
                            selectedImageIndex === 0
                                ? firstImage
                                : secondImage
                        }
                        className={`${
                            selectedImageIndex === 0
                                ? styles['slide-in-right']
                                : styles['slide-in-left']
                        }`}
                        alt={collectionName}
                        onClick={navigateToProductItem}
                    />
                </div>

                <footer>
                    <InventoryState
                        positive={isSoldOut}
                        label={
                            isSoldOut ? 'Sold Out' : 'In Stock'
                        }
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
                    text={`${formattedMinPrice} - ${formattedMaxPrice}`}
                    isLighter={true}
                />
                <StyledTextBlock
                    text={`${colorName} ${stoneName} set in ${metalName}`}
                    isSubtle={true}
                />
                <Stars rating={averageRating} fontSize={0.9} />
            </div>
        </article>
    );
};
