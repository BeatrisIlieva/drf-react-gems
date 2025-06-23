import { useParams } from 'react-router';
import { useProductItem } from '../api/productItemApi';
import type { ProductItemType } from '../types/Products';
import {
    useCallback,
    useEffect,
    useMemo,
    useState,
    type ReactNode
} from 'react';
import { ProductItemContext } from '../contexts/ProductItemContext';

interface Props {
    children: ReactNode;
}

export const ProductItemProvider = ({ children }: Props) => {
    const { getProductItem } = useProductItem();
    const { categoryName, productId } = useParams<{
        categoryName: string;
        productId: string;
    }>();
    const [loading, setLoading] = useState<boolean>(true);
    const [product, setProduct] =
        useState<ProductItemType | null>(null);
    const [selectedSize, setSelectedSize] = useState<
        number | null
    >(null);
    const [notSelectedSizeError, setNotSelectedSizeError] =
        useState<boolean | null>(null);

    useEffect(() => {
        setLoading(true);
        getProductItem({ categoryName, productId })
            .then((response) => {
                setProduct(response.product);
            })
            .catch((error) => {
                console.error(
                    'Error fetching product item:',
                    error
                );
            })
            .finally(() => {
                setLoading(false);
            });
    }, [categoryName, productId, getProductItem]);

    const addToBagHandler = useCallback((): void => {
        if (selectedSize === null) {
            setNotSelectedSizeError(true);
            return;
        }
    }, [selectedSize]);

    const addToWishlistHandler = (): void => {};

    const setSelectedSizeHandler = useCallback((size: number): void => {
        if (selectedSize === null) {
            setSelectedSize(size);
            setNotSelectedSizeError(false);
        } else if (selectedSize === size) {
            setSelectedSize(null);
            setNotSelectedSizeError(null);
        } else {
            setSelectedSize(size);
            setNotSelectedSizeError(false);
        }
    }, [selectedSize]);

    const contextValue = useMemo(
        () => ({
            firstImage: product?.firstImage,
            secondImage: product?.secondImage,
            averageRating: product?.averageRating,
            reviews: product?.review,
            productId: product?.id,
            collectionName: product?.collection.name,
            colorName: product?.color.name,
            stoneName: product?.stone.name,
            metalName: product?.metal.name,
            inventory: product?.inventory,
            relatedProducts: product?.relatedProducts,
            relatedCollectionProducts:
                product?.relatedCollectionProducts,
            loading,
            product,
            selectedSize,
            setSelectedSizeHandler,
            addToBagHandler,
            addToWishlistHandler,
            notSelectedSizeError
        }),
        [
            product,
            loading,
            selectedSize,
            addToBagHandler,
            setSelectedSizeHandler,
            notSelectedSizeError
        ]
    );

    return (
        <ProductItemContext.Provider value={contextValue}>
            {children}
        </ProductItemContext.Provider>
    );
};
