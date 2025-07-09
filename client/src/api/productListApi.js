import { useCallback } from "react";
import { useApi } from "../hooks/useApi";
import { keysToCamelCase } from "../utils/convertToCamelCase";

import { HOST } from "../constants/host";

const baseUrl = `${HOST}/api/products`;

export const useProductList = () => {
    const { get } = useApi();

    const getProductList = useCallback(
        async ({
            categoryName,
            ordering = null,
            page = null,
            colorIds = [],
            stoneIds = [],
            metalIds = [],
            collectionIds = [],
        }) => {
            const params = new URLSearchParams();

            if (page) params.append("page", page.toString());
            if (ordering) params.append("ordering", ordering);
            if (colorIds) {
                colorIds.forEach((id) =>
                    params.append("colors", id.toString()),
                );
            }
            if (stoneIds) {
                stoneIds.forEach((id) =>
                    params.append("stones", id.toString()),
                );
            }
            if (metalIds) {
                metalIds.forEach((id) =>
                    params.append("metals", id.toString()),
                );
            }
            if (collectionIds) {
                collectionIds.forEach((id) =>
                    params.append("collections", id.toString()),
                );
            }

            const queryString = params.toString();
            const fullUrl = queryString
                ? `${baseUrl}/${categoryName}/?${queryString}`
                : `${baseUrl}/${categoryName}/`;

            try {
                const response = await get(fullUrl);

                return keysToCamelCase(response);
            } catch (error) {
                console.error(error);
            }
        },
        [get],
    );

    return { getProductList };
};
