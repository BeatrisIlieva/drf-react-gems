/**
 * Standardized error handling utility for API calls
 * Provides consistent error logging and response formatting
 */

export const handleApiError = (
    error,
    operation,
    fallbackValue = undefined
) => {
    const errorMessage =
        error instanceof Error ? error.message : String(error);
    console.error(`Error in ${operation}:`, errorMessage);

    // For authentication errors, rethrow to allow auth refresh
    if (error?.status === 401) {
        throw error;
    }

    return fallbackValue;
};

export const handleApiSuccess = (response, transform = null) => {
    if (transform && typeof transform === 'function') {
        return transform(response);
    }
    return response;
};

/**
 * Wrapper for API calls with standardized error handling
 * @param {Function} apiCall - The API function to call
 * @param {string} operation - Description of the operation for logging
 * @param {any} fallbackValue - Value to return on error
 * @param {Function} transform - Optional transformation function for success response
 */
export const withErrorHandling = async (
    apiCall,
    operation,
    fallbackValue = undefined,
    transform = null
) => {
    try {
        const response = await apiCall();
        return handleApiSuccess(response, transform);
    } catch (error) {
        return handleApiError(error, operation, fallbackValue);
    }
};
