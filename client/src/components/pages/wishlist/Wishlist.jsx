import { EmptyList } from '../../reusable/empty-list/EmptyList';
import { ProductItems } from '../../reusable/product-items/ProductItems';

import { useWishlistContext } from '../../../contexts/WishlistContext';

import styles from './Wishlist.module.scss';

export const Wishlist = () => {
    const { wishlistItems, loading, wishlistItemsCount } = useWishlistContext();

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
                            <ProductItems products={wishlistItems} />
                        </section>
                    ) : (
                        <EmptyList title="Wishlist" />
                    )}
                </>
            )}
        </>
    );
};
