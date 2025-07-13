import { useCallback } from 'react';

import { useApi } from '../hooks/useApi';

import { keysToCamelCase } from '../utils/convertToCamelCase';

import { HOST } from '../constants/host';

const baseUrl = `${HOST}/api/products`;

const USE_ASYNC_FILTERS = true;

export const useFilters = () => {
    const { get } = useApi();

    /**
     * Fetches filter data from the backend.
     * Tries the async endpoint first (if enabled), falls back to sync if async fails.
     *
     * @param {Object} params - Filter params
     * @returns {Promise<Object>} - Filter data in camelCase keys
     */
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

            let fullUrl = `${baseUrl}/${entityName}/async/?${queryString}`;

            try {
                if (USE_ASYNC_FILTERS) {
                    const response = await get(fullUrl);
                    return keysToCamelCase(response);
                }
            } catch (error) {
                console.warn('Async filter endpoint failed, falling back to sync:', error);
                fullUrl = `${baseUrl}/${entityName}/?${queryString}`;
                try {
                    const response = await get(fullUrl);
                    return keysToCamelCase(response);
                } catch (syncError) {
                    console.error('Both async and sync filter endpoints failed:', syncError);
                    throw syncError;
                }
            }
        },
        [get]
    );

    return { getFilters };
};
