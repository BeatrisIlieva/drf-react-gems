import { useWishlistContext } from '../../../contexts/WishlistContext';
import { ProductItems } from '../../reusable/product-items/ProductItems';
import { Skeleton } from '../product-list/skeleton/Skeleton';

export const Wishlist = () => {
    const { wishlistItems, isLoading } = useWishlistContext();

    return (
        <>
            {isLoading &&
            (!wishlistItems || wishlistItems.length === 0) ? (
                <Skeleton />
            ) : (
                <ProductItems products={wishlistItems} />
            )}
        </>
    );
};
