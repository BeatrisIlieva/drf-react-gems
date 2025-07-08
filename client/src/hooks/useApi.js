import { useContext, useCallback, useMemo } from 'react';

import { useAuthRefresh } from './auth/useAuthRefresh';
import { useGuest } from './useGuest';

import { UserContext } from '../contexts/UserContext';

export const useApi = () => {
    const { access, refresh } = useContext(UserContext);
    const { authRefresh } = useAuthRefresh();
    const { getGuestData } = useGuest();

    const request = useCallback(
        async (
            method,
            url,
            {
                data = null,
                accessRequired = false,
                refreshRequired = false,
                contentType = 'application/json'
            } = {}
        ) => {
            const options = {
                method,
                headers: {
                    'Content-Type': contentType
                }
            };

            // Get guest ID dynamically to ensure we have the latest value
            const currentGuestId = getGuestData();
            if (currentGuestId) {
                options.headers['Guest-Id'] = currentGuestId;
            }

            if (accessRequired) {
                options.headers.Authorization = `Bearer ${access}`;
            }

            if (method !== 'GET') {
                let bodyData = data;

                if (contentType === 'multipart/form-data') {
                    if (!(bodyData instanceof FormData)) {
                        throw new Error(
                            'Data must be a FormData instance for multipart/form-data'
                        );
                    }

                    if (refreshRequired) {
                        if (refresh) {
                            bodyData.append('refresh', refresh);
                        }
                    }

                    options.body = bodyData;

                    delete options.headers['Content-Type'];
                } else {
                    if (refreshRequired && refresh) {
                        bodyData = { ...bodyData, refresh };
                    }

                    options.body = JSON.stringify(bodyData);
                }
            }

            const response = await fetch(url, options);

            // Check if response has content before trying to parse JSON
            let json = null;
            const responseContentType =
                response.headers.get('content-type');
            const hasContent =
                response.status !== 204 &&
                response.status !== 205 &&
                responseContentType &&
                responseContentType.includes('application/json');

            if (hasContent) {
                const responseText = await response.text();
                if (responseText && responseText.trim()) {
                    try {
                        json = JSON.parse(responseText);
                    } catch {
                        console.warn(
                            'Failed to parse JSON response:',
                            responseText
                        );
                        json = null;
                    }
                }
            }

            if (!response.ok) {
                if (response.status === 401) {
                    if (json?.error === 'Invalid username or password') {
                        return 'Invalid username or password';
                    }
                    
                    try {
                        await authRefresh();
                        
                        // Wait a small amount for localStorage to be updated
                        await new Promise(resolve => setTimeout(resolve, 50));
                        
                        const newGuestId = getGuestData();
                        const retryOptions = {
                            method: options.method,
                            headers: {
                                'Content-Type': options.headers['Content-Type']
                            }
                        };
                        
                        // Get fresh auth data after refresh
                        const authDataString = localStorage.getItem('auth');
                        if (authDataString) {
                            try {
                                const authData = JSON.parse(authDataString);
                                if (authData.access) {
                                    retryOptions.headers.Authorization = `Bearer ${authData.access}`;
                                }
                            } catch (e) {
                                console.error('Failed to parse auth data:', e);
                            }
                        }
                        
                        if (newGuestId) {
                            retryOptions.headers['Guest-Id'] = newGuestId;
                        }
                        
                        // Include body if it was in original request
                        if (options.body) {
                            retryOptions.body = options.body;
                        }
                        
                        const retryResponse = await fetch(url, retryOptions);
                        
                        let retryJson = null;
                        const retryContentType = retryResponse.headers.get('content-type');
                        const retryHasContent = retryResponse.status !== 204 && 
                                               retryResponse.status !== 205 && 
                                               retryContentType && 
                                               retryContentType.includes('application/json');
                        
                        if (retryHasContent) {
                            const retryResponseText = await retryResponse.text();
                            if (retryResponseText && retryResponseText.trim()) {
                                try {
                                    retryJson = JSON.parse(retryResponseText);
                                } catch {
                                    console.warn('Failed to parse retry JSON response:', retryResponseText);
                                    retryJson = null;
                                }
                            }
                        }
                        
                        if (!retryResponse.ok) {
                            console.error('Retry failed with status:', retryResponse.status);
                            const retryError = new Error(
                                retryJson?.message || 
                                retryJson?.error || 
                                `HTTP ${retryResponse.status}: ${retryResponse.statusText}`
                            );
                            retryError.status = retryResponse.status;
                            retryError.data = retryJson;
                            retryError.url = url;
                            throw retryError;
                        }
                        
                        return retryJson;
                        
                    } catch (refreshError) {
                        console.error('Token refresh failed:', refreshError);
                        throw refreshError;
                    }
                }

                const error = new Error(
                    json?.message ||
                        json?.error ||
                        `HTTP ${response.status}: ${response.statusText}`
                );
                error.status = response.status;
                error.data = json;
                error.url = url;
                throw error;
            }

            return json;
        },
        [access, refresh, authRefresh, getGuestData]
    );

    return useMemo(
        () => ({
            get: request.bind(null, 'GET'),
            post: request.bind(null, 'POST'),
            put: request.bind(null, 'PUT'),
            patch: request.bind(null, 'PATCH'),
            del: request.bind(null, 'DELETE')
        }),
        [request]
    );
};


// import { useContext, useCallback, useMemo } from 'react';
// import { UserContext } from '../contexts/UserContext';
// import { useAuthRefresh } from './auth/useAuthRefresh';
// import { useGuest } from './useGuest';

// export const useApi = () => {
//     const { access, refresh } = useContext(UserContext);
//     const { authRefresh } = useAuthRefresh();
//     const { getGuestData } = useGuest();

//     const guestId = useMemo(() => getGuestData(), [getGuestData]);

//     const request = useCallback(
//         async (
//             method,
//             url,
//             {
//                 data = null,
//                 accessRequired = false,
//                 refreshRequired = false,
//                 contentType = 'application/json'
//             } = {}
//         ) => {
//             const options = {
//                 method,
//                 headers: {
//                     'Content-Type': contentType,
//                 }
//             };

//             if (guestId) {
//                 options.headers['Guest-Id'] = guestId;
//             }

//             if (accessRequired) {
//                 options.headers.Authorization = `Bearer ${access}`;
//             }

//             if (method !== 'GET') {
//                 let bodyData = data;

//                 if (contentType === 'multipart/form-data') {
//                     if (!(bodyData instanceof FormData)) {
//                         throw new Error(
//                             'Data must be a FormData instance for multipart/form-data'
//                         );
//                     }

//                     if (refreshRequired) {
//                         bodyData.append('refresh', refresh);
//                     }

//                     options.body = bodyData;

//                     delete options.headers['Content-Type'];
//                 } else {
//                     if (refreshRequired) {
//                         bodyData = { ...bodyData, refresh };
//                     }

//                     options.body = JSON.stringify(bodyData);
//                 }
//             }

//             const response = await fetch(url, options);

//             const json = await response.json();

//             if (!response.ok) {
//                 if (response.status === 401) {
//                     if (json.error === 'Invalid username or password') {
//                         return 'Invalid username or password';
//                     }

//                     await authRefresh();
//                 }

//                 const error = new Error('Request failed');
//                 error.status = response.status;
//                 error.data = json;
//                 throw error;
//             }

//             return json;
//         },
//         [access, refresh, authRefresh, guestId]
//     );

//     return useMemo(
//         () => ({
//             get: request.bind(null, 'GET'),
//             post: request.bind(null, 'POST'),
//             put: request.bind(null, 'PUT'),
//             patch: request.bind(null, 'PATCH'),
//             del: request.bind(null, 'DELETE')
//         }),
//         [request]
//     );
// };