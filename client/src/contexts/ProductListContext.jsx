import { createContext, useContext } from "react";

export const ProductListContext = createContext({
    count: 0,
    ordering: null,
    loading: false,
    error: null,
    loadMoreDisabled: false,
    products: [],
    loadMoreHandler: () => null,
    updateOrdering: () => null,
});

export const useProductListContext = () => {
    const data = useContext(ProductListContext);

    return data;
};
