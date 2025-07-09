import { useState, useEffect, useCallback } from "react";
import { keysToCamelCase } from "../utils/convertToCamelCase";

export const useFormDataLoader = (
    loadDataFn,
    updateFieldValue,
    fieldConfig,
) => {
    const [loading, setLoading] = useState(true);
    const [initialDataLoaded, setInitialDataLoaded] = useState(false);

    const loadInitialData = useCallback(async () => {
        if (initialDataLoaded || !loadDataFn) return;

        try {
            const data = await loadDataFn();
            if (data) {
                const camelCaseData = keysToCamelCase(data);

                Object.keys(fieldConfig).forEach((fieldName) => {
                    const value = camelCaseData[fieldName];
                    if (value !== undefined && value !== null && value !== "") {
                        updateFieldValue(fieldName, value, false);
                    }
                });
            }
            setInitialDataLoaded(true);
        } finally {
            setLoading(false);
        }
    }, [loadDataFn, updateFieldValue, fieldConfig, initialDataLoaded]);

    useEffect(() => {
        loadInitialData();
    }, [loadInitialData]);

    return { loading, initialDataLoaded };
};
