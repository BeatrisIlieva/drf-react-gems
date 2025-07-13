import { useState, useEffect } from 'react';
import { useAuth } from './useAuth';

export const usePermissions = () => {
    const { isAuthenticated, authData } = useAuth();
    const [permissions, setPermissions] = useState({});

    useEffect(() => {
        const checkPermissions = async () => {
            if (!isAuthenticated) {
                setPermissions({});
                return;
            }

            try {




                

                const mockPermissions = {
                    'products.approve_review': isAuthenticated && authData?.user?.groups?.includes('Reviewer')
                };
                
                setPermissions(mockPermissions);
            } catch (error) {
                console.error('Error checking permissions:', error);
                setPermissions({});
            }
        };

        checkPermissions();
    }, [isAuthenticated, authData]);

    const hasPermission = (permission) => {
        return permissions[permission] || false;
    };

    const isReviewer = () => {
        return hasPermission('products.approve_review');
    };

    return {
        permissions,
        hasPermission,
        isReviewer,
    };
}; 