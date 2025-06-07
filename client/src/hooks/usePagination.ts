import { useCallback, useState } from 'react';
import { getNextPageNumber } from '../utils/getNextPageNumber';

export const usePagination = () => {
    const [nextPage, setNextPage] = useState<number | null>(null);

    const updatePage = useCallback((next: string | null) => {
        const pageNumber = getNextPageNumber(next);
        setNextPage(pageNumber);
    }, []);

    return {
        nextPage,
        updatePage
    };
};
