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
import { useAddToShoppingBag } from '../api/shoppingBagApi';
import type { AddToBagParams } from '../types/ShoppingBag';

interface Props {
    children: ReactNode;
}

export const ProductItemProvider = ({ children }: Props) => {
    const { getProductItem } = useProductItem();
    const { categoryName, productId } = useParams<{
        categoryName: string;
        productId: string;
    }>();
    const { addToBag } = useAddToShoppingBag();

    const [loading, setLoading] = useState<boolean>(true);
    const [product, setProduct] =
        useState<ProductItemType | null>(null);
    const [selectedSize, setSelectedSize] = useState<
        number | null
    >(null);
    const [notSelectedSizeError, setNotSelectedSizeError] =
        useState<boolean | null>(null);
    const [selectedInventory, setSelectedInventory] =
        useState<AddToBagParams | null>(null);

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

        addToBag(selectedInventory!);
    }, [selectedSize, addToBag, selectedInventory]);

    const addToWishlistHandler = (): void => {};

    const updateSelectedInventoryHandler = (
        contentType: string,
        objectId: number
    ) => {
        setSelectedInventory({
            quantity: 1,
            contentType,
            objectId
        });
    };

    const setSelectedSizeHandler = useCallback(
        (
            size: number,
            contentType: string,
            objectId: number
        ): void => {
            if (selectedSize === null) {
                setSelectedSize(size);
                setNotSelectedSizeError(false);
                updateSelectedInventoryHandler(
                    contentType,
                    objectId
                );
            } else if (selectedSize === size) {
                setSelectedSize(null);
                setNotSelectedSizeError(null);
                setSelectedInventory(null);
            } else {
                setSelectedSize(size);
                setNotSelectedSizeError(false);
                updateSelectedInventoryHandler(
                    contentType,
                    objectId
                );
            }
        },
        [selectedSize]
    );

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
