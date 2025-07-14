import { useEffect, useState } from 'react';

import { Popup } from '../../../reusable/popup/Popup';
import { UserAction } from '../../product-item/main-content/user-action/UserAction';

import { useProductItem } from '../../../../api/productItemApi';

import { ProductDataProvider } from '../../../../providers/ProductDataProvider';

import { useProductItemContext } from '../../../../contexts/ProductItemContext';
import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';
import { useWishlistContext } from '../../../../contexts/WishlistContext';

function normalizeProductData(data) {
    if (!data) return {};
    return {
        id: data.id || data.productId || '',
        firstImage: data.firstImage || '',
        secondImage: data.secondImage || '',
        averageRating: data.averageRating || 0,
        review: data.reviews || [],
        collection: data.collection || { name: data.collectionName || '' },
        color: data.color || { name: data.colorName || '' },
        stone: data.stone || { name: data.stoneName || '' },
        metal: data.metal || { name: data.metalName || '' },
        inventory: Array.isArray(data.inventory) ? data.inventory : [],
        relatedProducts: Array.isArray(data.relatedProducts) ? data.relatedProducts : [],
        relatedCollectionProducts: Array.isArray(data.relatedCollectionProducts)
            ? data.relatedCollectionProducts
            : [],
        categoryName: data.categoryName || '',
    };
}

export const WishlistProductPopup = ({ isOpen, onClose, productData, categoryName, productId }) => {
    const { removeFromWishlist } = useWishlistContext();
    const [isAddingToBag, setIsAddingToBag] = useState(false);
    const { getProductItem } = useProductItem();
    const [fullProductData, setFullProductData] = useState(null);
    const [loading, setLoading] = useState(false);
    const { openMiniBagPopup } = useShoppingBagContext();

    useEffect(() => {
        const pluralCategoryName =
            categoryName && !categoryName.endsWith('s') ? `${categoryName}s` : categoryName;
        if (isOpen && pluralCategoryName && productId) {
            setLoading(true);
            getProductItem({ categoryName: pluralCategoryName, productId })
                .then(response => {
                    setFullProductData(response?.product || null);
                })
                .finally(() => setLoading(false));
        }

        if (!isOpen) {
            setFullProductData(null);
        }
    }, [isOpen, categoryName, productId, getProductItem]);

    if (!isOpen || !productData) {
        return null;
    }

    const normalizedProductData = fullProductData
        ? normalizeProductData(fullProductData)
        : normalizeProductData(productData);

    function AddToBagWrapper() {
        const { createShoppingBagHandler } = useProductItemContext();

        const wrappedAddToBag = async () => {
            const result = await createShoppingBagHandler();

            if (result !== false) {
                openMiniBagPopup();
                await removeFromWishlist(categoryName, productId);
                onClose();
            }
        };
        return (
            <UserAction
                onAddToBag={wrappedAddToBag}
                isAddingToBag={isAddingToBag}
                categoryName={
                    normalizedProductData.contentType || normalizedProductData.categoryName
                }
                hideWishlistButton={true}
            />
        );
    }

    return (
        <Popup isOpen={isOpen} onClose={onClose}>
            {!loading && fullProductData ? (
                <ProductDataProvider
                    productData={normalizeProductData(fullProductData)}
                    categoryName={categoryName}
                    productId={productId}
                >
                    <AddToBagWrapper />
                </ProductDataProvider>
            ) : null}
        </Popup>
    );
};
