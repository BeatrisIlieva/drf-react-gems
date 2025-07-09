import { useCallback, useState } from 'react';
import { getNextPageNumber } from '../utils/getNextPageNumber';

export const usePagination = () => {
    const [nextPage, setNextPage] = useState(null);

    const updatePage = useCallback((next) => {
        const pageNumber = getNextPageNumber(next);
        setNextPage(pageNumber);
    }, []);

    return {
        nextPage,
        updatePage
    };
};
