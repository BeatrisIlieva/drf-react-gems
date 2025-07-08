import { useCallback, useEffect, useState } from 'react';
import { useCategoryName } from '../../../../hooks/products/useCategoryName';
import { formatPrice } from '../../../../utils/formatPrice';
import { useNavigate } from 'react-router';
import { useWishlistContext } from '../../../../contexts/WishlistContext';
import styles from './ProductCard.module.scss';
import { Icon } from '../../icon/Icon';
import { InventoryState } from './inventory-state/InventoryState';
import { ToggleImageButtons } from './toggle-image-buttons/ToggleImageButtons';
import { StyledTextBlock } from '../../styled-text-block/StyledTextBlock';
import { Stars } from '../../stars/Stars';
import { ProductItems } from '../ProductItems';

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
    averageRating,
    categoryName
}) => {
    const [selectedImageIndex, setSelectedImageIndex] =
        useState(0);
    const { categoryName: categoryFromUrl } = useCategoryName();
    const formattedMinPrice = formatPrice(minPrice);
    const formattedMaxPrice = formatPrice(maxPrice);
    const navigate = useNavigate();
    const { isInWishlist, handleWishlistToggle } =
        useWishlistContext();
    const categoryParam = categoryFromUrl
        ? categoryFromUrl
        : categoryName;
    const category = categoryParam?.slice(
        0,
        categoryParam?.length - 1
    );

    const isItemInWishlist = isInWishlist(category, id);

    const navigateToProductItem = useCallback(() => {
        navigate(`/products/${categoryParam}/${id}`);
    }, [categoryParam, id, navigate]);

    useEffect(() => {
        setSelectedImageIndex(0);
    }, [categoryName]);

    const capitalizedCategoryName =
        categoryParam.charAt(0).toUpperCase() +
        categoryParam.slice(1, categoryParam.length - 1);

    return (
        <article className={styles['product-card']}>
            <div className={styles['wrapper']}>
                <button
                    onClick={() =>
                        handleWishlistToggle(`${category}s`, id)
                    }
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
                    text={`${collectionName} ${capitalizedCategoryName}`}
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
