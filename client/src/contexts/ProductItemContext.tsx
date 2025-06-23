import { createContext, useContext } from 'react';
import type {
    InventoryItem,
    ProductItemType,
    RelatedProductType,
    Review
} from '../types/Products';

interface ProductItemContextType {
    firstImage?: string;
    secondImage?: string;
    averageRating?: number;
    reviews?: Review[];
    productId?: number;
    collectionName?: string;
    colorName?: string;
    stoneName?: string;
    metalName?: string;
    inventory?: InventoryItem[];
    relatedCollectionProducts?: ProductItemType[];
    relatedProducts?: RelatedProductType[];
    loading?: boolean;
    selectedSize: number | null;
    setSelectedSizeHandler: (
        size: number,
        contentType: string,
        objectId: number
    ) => void;
    createShoppingBagHandler: () => void;
    addToWishlistHandler: () => void;
    notSelectedSizeError: boolean | null;
}

export const ProductItemContext =
    createContext<ProductItemContextType>({
        firstImage: '',
        secondImage: '',
        averageRating: 0,
        reviews: [],
        productId: 0,
        collectionName: '',
        colorName: '',
        stoneName: '',
        metalName: '',
        inventory: [],
        relatedCollectionProducts: [],
        relatedProducts: [],
        loading: true,
        selectedSize: null,
        setSelectedSizeHandler: () => null,
        createShoppingBagHandler: () => null,
        addToWishlistHandler: () => null,
        notSelectedSizeError: null
    });

export const useProductItemContext = () => {
    const data = useContext(ProductItemContext);

    return data;
};
