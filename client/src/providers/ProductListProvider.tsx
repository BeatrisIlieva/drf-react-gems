import { type ReactNode } from 'react';

import { ProductListContext } from '../contexts/ProductListContext';
import { useProductData } from '../hooks/useProductData';
import { useProductFilters } from '../hooks/useProductFilters';
import { useProductOrdering } from '../hooks/useProductOrdering';

interface Props {
    children: ReactNode;
}

export const ProductListProvider = ({ children }: Props) => {
    const {
        products,
        collections,
        colors,
        count,
        metals,
        stones,
        loading,
        error,
        fetchProducts,
        page,
        loadMoreDisabled,
        loadMoreHandler,
        resetPage
    } = useProductData();

    const {
        toggleDisplayFilters,
        updateEntityCharacteristics,
        entityStateMapper,
        displayFilters,
        colorIds,
        stoneIds,
        metalIds,
        collectionIds
    } = useProductFilters();

    const { orderingCriteria, updateOrderingCriteria } = useProductOrdering();

    return (
        <ProductListContext.Provider
            value={{
                products,
                collections,
                colors,
                count,
                metals,
                page,
                stones,
                colorIds,
                stoneIds,
                metalIds,
                collectionIds,
                loading,
                error,
                fetchProducts,
                loadMoreHandler,
                loadMoreDisabled,
                updateEntityCharacteristics,
                entityStateMapper,
                toggleDisplayFilters,
                displayFilters,
                updateOrderingCriteria,
                orderingCriteria,
                resetPage
            }}
        >
            {children}
        </ProductListContext.Provider>
    );
};
