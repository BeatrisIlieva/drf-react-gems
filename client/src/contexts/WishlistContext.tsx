import { createContext, useContext } from 'react';
import type { WishlistItem } from '../types/Wishlist';

export interface WishlistContextType {
    wishlistItems: WishlistItem[];
    wishlistCount: number;
    isLoading: boolean;
    addToWishlist: (contentType: string, objectId: number) => Promise<boolean>;
    removeFromWishlist: (contentType: string, objectId: number) => Promise<boolean>;
    isInWishlist: (contentType: string, objectId: number) => boolean;
    refreshWishlist: () => Promise<void>;
    updateWishlistCount: () => Promise<void>;
}

export const WishlistContext = createContext<WishlistContextType>({
    wishlistItems: [],
    wishlistCount: 0,
    isLoading: false,
    addToWishlist: async () => false,
    removeFromWishlist: async () => false,
    isInWishlist: () => false,
    refreshWishlist: async () => {},
    updateWishlistCount: async () => {},
});

export const useWishlistContext = () => {
    const data = useContext(WishlistContext);

    return data;
};
