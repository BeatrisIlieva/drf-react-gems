import { useCallback, useState } from 'react';

export const useOrdering = () => {
    const [ordering, setOrdering] = useState<string | null>(null);

    const updateOrdering = useCallback((criteria: string) => {
        setOrdering(criteria);
    }, []);

    const resetOrdering = useCallback(() => {
        setOrdering(null);
    }, []);

    return {
        ordering,
        updateOrdering,
        resetOrdering
    };
};
