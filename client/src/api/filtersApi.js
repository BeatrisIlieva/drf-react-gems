import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/products`;

export const useFilters = () => {
    const { get } = useApi();
    const getFilters = useCallback(
        async ({
            categoryName,
            entityName,
            colorIds = [],
            stoneIds = [],
            metalIds = [],
            collectionIds = [],
        }) => {
            const params = new URLSearchParams();

            if (colorIds) {
                colorIds.forEach(id => params.append('colors', id.toString()));
            }
            if (stoneIds) {
                stoneIds.forEach(id => params.append('stones', id.toString()));
            }
            if (metalIds) {
                metalIds.forEach(id => params.append('metals', id.toString()));
            }
            if (collectionIds) {
                collectionIds.forEach(id => params.append('collections', id.toString()));
            }

            params.append('category', categoryName || '');

            const queryString = params.toString();

            let fullUrl = `${baseUrl}/${entityName}/?${queryString}`;

            try {
                const response = await get(fullUrl);
                return keysToCamelCase(response);
            } catch (error) {
                console.error('Error fetching filters:', error);
                return null;
            }
        },
        [get]
    );

    return { getFilters };
};
