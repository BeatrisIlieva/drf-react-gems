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

    const [product, setProduct] =
        useState<ProductItemType | null>(null);

    useEffect(() => {
        getProductItem({ categoryName, productId })
            .then((response) => {
                setProduct(response.product);
            })
            .catch((error) => {
                console.error(
                    'Error fetching product item:',
                    error
                );
            });
    }, [categoryName, productId, getProductItem]);

    const contextValue = useMemo(
        () => ({
            firstImage: product!.firstImage,
            secondImage: product!.secondImage,
            averageRating: product!.averageRating,
            reviews: product!.review,
            productId: product!.id,
            collectionName: product!.collection.name,
            colorName: product!.color.name,
            stoneName: product!.stone.name,
            metalName: product!.metal.name,
            inventory: product!.inventory,
            relatedProducts: product!.relatedProducts,
            relatedCollectionProducts:
                product!.relatedCollectionProducts
        }),
        [product]
    );

    return (
        <ProductItemContext.Provider value={contextValue}>
            {children}
        </ProductItemContext.Provider>
    );
};
