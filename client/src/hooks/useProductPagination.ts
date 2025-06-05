import { useEffect, useState } from 'react';

import { useCategoryName } from './useCategoryName';
import { useProductListContext } from '../contexts/ProductListContext';

export const useProductPagination = () => {
    const { categoryName } = useCategoryName();
    const { count, products} = useProductListContext();

    const [page, setPage] = useState<number>(1);
    const [loadMoreDisabled, setLoadMoreDisabled] = useState<boolean>(false);

    const resetPage = () => {
        setPage(1);
    };
    

    const loadMoreHandler = (): void => {
        if (count <= products.length) {
            setLoadMoreDisabled(true);
            return;
        }

        const nextPage = page + 1;
        setPage(nextPage);
    };

    useEffect(() => {
        resetPage();
        setLoadMoreDisabled(false);
    }, [categoryName]);

    useEffect(() => {
        if (products.length > 0) {
            if (count <= products.length) {
                setLoadMoreDisabled(true);
            } else {
                setLoadMoreDisabled(false);
            }
        }
    }, [count, products.length, page]);

    return {
        page,
        resetPage,
        loadMoreDisabled,
        loadMoreHandler
    };
};
