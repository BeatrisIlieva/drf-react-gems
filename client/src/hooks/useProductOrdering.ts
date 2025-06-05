import { useEffect, useState } from 'react';

import { useCategoryName } from './useCategoryName';

export const useProductOrdering = () => {
    const { categoryName } = useCategoryName();

    const [orderingCriteria, setOrderingCriteria] = useState<string>('rating');

    const updateOrderingCriteria = (criteria: string) => {
        setOrderingCriteria(criteria);
    };

    useEffect(() => {
        setOrderingCriteria('rating');
    }, [categoryName]);

    return {
        orderingCriteria,
        updateOrderingCriteria
    };
};
