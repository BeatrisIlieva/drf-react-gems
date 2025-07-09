import { useWishlistContext } from "../../../contexts/WishlistContext";
import { EmptyList } from "../../reusable/empty-list/EmptyList";
import { ProductItems } from "../../reusable/product-items/ProductItems";

import styles from "./Wishlist.module.scss";

export const Wishlist = () => {
    const { wishlistItems, loading } = useWishlistContext();

    return (
        <>
            {!loading && (
                <>
                    {wishlistItems.length > 0 ? (
                        <section className={styles["wishlist"]}>
                            <h2>Your Wishlist</h2>
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
