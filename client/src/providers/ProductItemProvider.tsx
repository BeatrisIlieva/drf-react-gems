import { useParams } from 'react-router';
import { useProductItem } from '../api/productItemApi';
import type { ProductItemType } from '../types/Products';
import {
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

    const addToBagHandler = (): void => {};

    const addToWishlistHandler = (): void => {};

    const setSelectedSizeHandler = (size: number): void => {
        if (selectedSize === null) {
            setSelectedSize(size);
        } else if (selectedSize === size) {
            setSelectedSize(null);
        } else {
            setSelectedSize(size);
        }
    };

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
            addToWishlistHandler
        }),
        [product, loading, selectedSize]
    );

    return (
        <ProductItemContext.Provider value={contextValue}>
            {children}
        </ProductItemContext.Provider>
    );
};
