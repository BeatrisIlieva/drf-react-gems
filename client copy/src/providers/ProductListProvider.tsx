import { type ReactNode, useMemo } from 'react';

import { ProductListContext } from '../contexts/ProductListContext';

import { useProductsData } from '../hooks/products/useProductsData';

interface Props {
    children: ReactNode;
}

export const ProductListProvider = ({ children }: Props) => {
    const productData = useProductsData();

    const contextValue = useMemo(() => ({ ...productData }), [productData]);

    return (
        <ProductListContext.Provider value={contextValue}>
            {children}
        </ProductListContext.Provider>
    );
};
