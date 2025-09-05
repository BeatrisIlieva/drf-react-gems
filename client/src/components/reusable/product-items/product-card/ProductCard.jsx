import { useCallback, useEffect, useState } from 'react';

import { useLocation, useNavigate } from 'react-router';

import { Icon } from '../../icon/Icon';
import { Stars } from '../../stars/Stars';
import { StyledTextBlock } from '../../styled-text-block/StyledTextBlock';
import { ToggleImageButtons } from './toggle-image-buttons/ToggleImageButtons';

import { useCategoryName } from '../../../../hooks/useCategoryName';

import { useWishlistContext } from '../../../../contexts/WishlistContext';

import { formatPrice } from '../../../../utils/formatPrice';

import styles from './ProductCard.module.scss';

export const ProductCard = ({
    id,
    collectionName,
    firstImage,
    secondImage,
    fourthImage,
    colorName,
    stoneName,
    metalName,
    minPrice,
    maxPrice,
    averageRating,
    categoryName,
    onMoveToBag, // New prop for handling move to bag
}) => {
    const location = useLocation();
    const [selectedImageIndex, setSelectedImageIndex] = useState(0);
    const { categoryName: categoryFromUrl } = useCategoryName();
    const formattedMinPrice = formatPrice(minPrice);
    const formattedMaxPrice = formatPrice(maxPrice);
    const navigate = useNavigate();
    const { isInWishlist, handleWishlistToggle } = useWishlistContext();
    const categoryParam = categoryFromUrl ? categoryFromUrl : categoryName;
    const category = categoryParam?.slice(0, categoryParam?.length - 1);

    const isItemInWishlist = isInWishlist(category, id);

    const isWishlistPage = location.pathname.includes('/wishlist');

    const navigateToProductItem = useCallback(() => {
        navigate(`/products/${categoryParam}/${id}`);
    }, [categoryParam, id, navigate]);

    const handleMoveToBag = useCallback(
        e => {
            e.stopPropagation(); // Prevent navigation
            if (onMoveToBag) {
                onMoveToBag({
                    id,
                    collectionName,
                    firstImage,
                    secondImage,
                    colorName,
                    stoneName,
                    metalName,
                    minPrice,
                    maxPrice,
                    averageRating,
                    categoryName: category,
                });
            }
        },
        [
            onMoveToBag,
            id,
            collectionName,
            firstImage,
            secondImage,
            colorName,
            stoneName,
            metalName,
            minPrice,
            maxPrice,
            averageRating,
            category,
        ]
    );

    useEffect(() => {
        setSelectedImageIndex(0);
    }, [categoryName]);

    const capitalizedCategoryName =
        categoryParam.charAt(0).toUpperCase() + categoryParam.slice(1, categoryParam.length - 1);

    return (
        <article className={styles['product-card']}>
            <div className={styles['wrapper']}>
                <button
                    onClick={() =>
                        handleWishlistToggle(
                            `${category}s`,
                            id,
                            collectionName,
                            firstImage,
                            secondImage,
                            colorName,
                            stoneName,
                            metalName,
                            minPrice,
                            maxPrice,
                            averageRating
                        )
                    }
                    className={styles['wishlist-button']}
                    aria-label={isItemInWishlist ? 'Remove from wishlist' : 'Add to wishlist'}
                >
                    {!isWishlistPage ? (
                        <Icon name={isItemInWishlist ? 'heart-filled' : 'heart'} />
                    ) : (
                        <Icon name="xMark" fontSize={0.9} isSubtle={true} />
                    )}
                </button>

                <div
                    className={styles['thumbnail']}
                    onMouseEnter={() => setSelectedImageIndex(1)}
                    onMouseLeave={() => setSelectedImageIndex(0)}
                >
                    <img
                        src={selectedImageIndex === 0 ? firstImage : fourthImage}
                        className={`${
                            selectedImageIndex === 0
                                ? styles['slide-in-right']
                                : styles['slide-in-left']
                        }`}
                        alt={collectionName}
                        onClick={navigateToProductItem}
                    />
                    {isWishlistPage && (
                        <button onClick={handleMoveToBag} className={styles['add-to-bag-button']}>
                            <span>Move to Bag</span>
                        </button>
                    )}
                </div>
                {secondImage && (
                    <footer>
                        <ToggleImageButtons
                            selectedIndex={selectedImageIndex}
                            onSelect={setSelectedImageIndex}
                        />
                    </footer>
                )}
            </div>
            <div className={styles['product-info']}>
                <StyledTextBlock text={`${collectionName} ${capitalizedCategoryName}`} />
                <StyledTextBlock
                    text={
                        maxPrice ? `${formattedMinPrice} - ${formattedMaxPrice}` : formattedMinPrice
                    }
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
