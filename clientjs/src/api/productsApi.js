import { useCallback } from 'react';
import { useApi } from '../hooks/useApi';

const baseUrl = 'http://localhost:8000/products';

export const useCategories = () => {
    const { get } = useApi();

    const getCategories = useCallback(async () => {
        try {
            const response = await get(`${baseUrl}/categories/`);

            return response;
        } catch (err) {
            console.error('Error in getCategories:', err.message);
            throw err;
        }
    }, [get]);

    return { getCategories };
};

// export const useProducts = () => {
//     const { get } = useApi();

//     const getProducts = useCallback(
//         async (
//             categoryId,
//             pageNumber = null,
//             colorId = null,
//             stoneId = null,
//             materialId = null
//         ) => {
//             const fullUrl = pageNumber
//                 ? `${baseUrl}/?category=${categoryId}&page=${pageNumber}`
//                 : `${baseUrl}/?category=${categoryId}`;

//             try {
//                 const response = await get(fullUrl);

//                 return response;
//             } catch (err) {
//                 console.error('Error in getProducts:', err.message);
//                 throw err;
//             }
//         },
//         [get]
//     );

//     return { getProducts };
// };

export const useProducts = () => {
    const { get } = useApi();

    const getProducts = useCallback(
        async ({
            categoryId,
            pageNumber = null,
            colorIds = [],
            stoneIds = [],
            stoneId = null,
            materialId = null
        }) => {
            const params = new URLSearchParams();

            if (categoryId) params.append('category', categoryId);
            if (pageNumber) params.append('page', pageNumber);
            if (colorIds) {
                colorIds.forEach((id) => params.append('color_ids', id));
            }
            if (stoneIds) {
                stoneIds.forEach((id) => params.append('stone_ids', id));
            }
            if (stoneId) params.append('stone', stoneId);
            if (materialId) params.append('material', materialId);

            const fullUrl = `${baseUrl}/?${params.toString()}`;

            try {
                const response = await get(fullUrl);
                return response;
            } catch (err) {
                console.error('Error in getProducts:', err.message);
                throw err;
            }
        },
        [get]
    );

    return { getProducts };
};
