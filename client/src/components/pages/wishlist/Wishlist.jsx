import { useState } from 'react';

import { EmptyList } from '../../reusable/empty-list/EmptyList';
import { ProductItems } from '../../reusable/product-items/ProductItems';
import { WishlistProductPopup } from './wishlist-product-popup/WishlistProductPopup';

import { useWishlistContext } from '../../../contexts/WishlistContext';

import styles from './Wishlist.module.scss';

export const Wishlist = () => {
    const { wishlistItems, loading, wishlistItemsCount } = useWishlistContext();
    const [selectedProduct, setSelectedProduct] = useState(null);

    const handleMoveToBag = productData => {
        setSelectedProduct(productData);
    };

    const handleClosePopup = () => {
        setSelectedProduct(null);
    };

    return (
        <>
            {!loading && (
                <>
                    {wishlistItems.length > 0 ? (
                        <section className={styles['wishlist']}>
                            <div className={styles['heading-wrapper']}>
                                <h2>Your Wishlist</h2>
                                <span>
                                    {wishlistItemsCount} {wishlistItemsCount > 1 ? 'items' : 'item'}
                                </span>
                            </div>
                            <ProductItems products={wishlistItems} onMoveToBag={handleMoveToBag} />
                        </section>
                    ) : (
                        <EmptyList title="Your Wishlist is empty." />
                    )}
                </>
            )}

            {selectedProduct && (
                <WishlistProductPopup
                    isOpen={!!selectedProduct}
                    onClose={handleClosePopup}
                    productData={selectedProduct}
                    categoryName={selectedProduct.categoryName}
                    productId={selectedProduct.id}
                />
            )}
        </>
    );
};
