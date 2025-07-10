import { useMemo } from 'react';

import { formatPrice } from '../utils/formatPrice';

export const usePriceCalculation = (inventory, selectedSize) => {
    const priceInfo = useMemo(() => {
        if (!inventory?.length) {
            return { formattedMinPrice: '', formattedMaxPrice: '', selectedInventoryItem: null };
        }

        const prices = inventory.map(item => parseFloat(item.price));
        const selectedInventoryItem = selectedSize
            ? inventory.find(item => item.size.id === selectedSize)
            : null;

        return {
            formattedMinPrice: formatPrice(Math.min(...prices).toString()),
            formattedMaxPrice: formatPrice(Math.max(...prices).toString()),
            selectedInventoryItem,
        };
    }, [inventory, selectedSize]);

    return priceInfo;
};
