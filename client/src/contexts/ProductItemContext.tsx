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
    setSelectedSizeHandler: (size: number) => void;
    addToBagHandler: () => void;
    addToWishlistHandler: () => void;
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
        addToBagHandler: () => null,
        addToWishlistHandler: () => null
    });

export const useProductItemContext = () => {
    const data = useContext(ProductItemContext);

    return data;
};
