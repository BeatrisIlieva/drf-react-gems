import { createContext, useContext } from "react";

export const WishlistContext = createContext({
    wishlistItems: [],
    wishlistItemsCount: 0,
    loading: false,
    addToWishlist: async () => false,
    removeFromWishlist: async () => false,
    isInWishlist: () => false,
    handleWishlistToggle: () => null,
    refreshWishlist: async () => null,
});

export const useWishlistContext = () => {
    const data = useContext(WishlistContext);

    return data;
};
