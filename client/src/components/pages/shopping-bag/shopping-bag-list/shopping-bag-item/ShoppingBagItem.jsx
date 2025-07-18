import { useCallback, useState } from 'react';

import { useLocation, useNavigate } from 'react-router';

import { QuantitySelector } from './quantity-selector/QuantitySelector';

import { useProductItemContext } from '../../../../../contexts/ProductItemContext';
import { useShoppingBagContext } from '../../../../../contexts/ShoppingBagContext';
import { useWishlistContext } from '../../../../../contexts/WishlistContext';

import { formatPrice } from '../../../../../utils/formatPrice';

import styles from './ShoppingBagItem.module.scss';

export const ShoppingBagItem = ({ quantity, totalPrice, productInfo, id, inventory }) => {
    const { deleteShoppingBagHandler, isDeleting } = useShoppingBagContext();
    const { addToWishlist, isInWishlist } = useWishlistContext();
    const { refreshProduct } = useProductItemContext();
    const [isMovingToWishlist, setIsMovingToWishlist] = useState(false);
    const navigate = useNavigate();
    const location = useLocation();

    const category = productInfo.category?.toLowerCase();
    const productId = productInfo.productId;
    const isItemInWishlist = isInWishlist(category, productId);
    const formattedTotalPricePerProduct = formatPrice(totalPrice.toString());

    const moveToWishListHandler = async () => {
        if (isMovingToWishlist || isDeleting || isItemInWishlist) return;

        setIsMovingToWishlist(true);
        try {
            const categoryValue = category.endsWith('s') ? category.slice(0, -1) : category;

            const success = await addToWishlist(categoryValue, productId);
            if (success) {
                await deleteShoppingBagHandler(id);

                if (location.pathname.includes(`/products/${category}s/${productId}`)) {
                    refreshProduct();
                }
            }
        } catch (error) {
            console.error('Error moving item to wishlist:', error);
        } finally {
            setIsMovingToWishlist(false);
        }
    };

    const handleRemove = async () => {
        await deleteShoppingBagHandler(id);

        if (location.pathname.includes(`/products/${category}s/${productId}`)) {
            refreshProduct();
        }
    };

    const navigateToProductItem = useCallback(() => {
        navigate(`/products/${productInfo.category.toLowerCase() + 's'}/${productInfo.productId}`);
    }, [navigate, productInfo.category, productInfo.productId]);

    return (
        <li className={styles['shopping-bag-item']}>
            <span className={styles['thumbnail']} onClick={navigateToProductItem}>
                <img src={productInfo.firstImage} alt={productInfo.collection} />
            </span>

            <span>
                <span>
                    <span>{`${productInfo.collection} ${productInfo.category}`}</span>

                    <span>
                        {`${productInfo.color} ${productInfo.stone} set in ${productInfo.metal}`}
                    </span>

                    <span>
                        <span>Size: {productInfo.size}</span>
                    </span>
                </span>

                <span>
                    <button
                        id={styles['move-to-wishlist']}
                        onClick={moveToWishListHandler}
                        disabled={isDeleting || isMovingToWishlist || isItemInWishlist}
                        className={
                            isItemInWishlist
                                ? styles['in-wishlist']
                                : isDeleting || isMovingToWishlist
                                  ? styles['removing']
                                  : ''
                        }
                    >
                        {isMovingToWishlist
                            ? 'Moving...'
                            : isItemInWishlist
                              ? 'In Wishlist'
                              : 'Move to Wish List'}
                    </button>
                    <button
                        onClick={handleRemove}
                        disabled={isDeleting}
                        className={isDeleting ? styles['removing'] : ''}
                    >
                        {isDeleting ? 'Removing...' : 'Remove'}
                    </button>
                </span>
            </span>

            <span>
                <span>{`${formattedTotalPricePerProduct}`}</span>
                <QuantitySelector
                    quantity={quantity}
                    id={id}
                    inventory={inventory}
                    availableQuantity={productInfo.availableQuantity}
                />
            </span>
        </li>
    );
};
