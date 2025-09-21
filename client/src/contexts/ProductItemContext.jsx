import { createContext, useContext } from 'react';

export const ProductItemContext = createContext({
    firstImage: '',
    secondImage: '',
    thirdImage: '',
    fourthImage: '',
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
    createShoppingBagHandler: async () => {},
    notSelectedSizeError: null,
    addToCartError: null,
    isSoldOut: false,
    isMiniBagPopupOpen: false,
    toggleMiniBagPopupOpen: () => {},
    refreshProduct: async () => {},
});

export const useProductItemContext = () => {
    const data = useContext(ProductItemContext);

    return data;
};
