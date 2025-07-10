import { useState } from 'react';

import { DeleteButton } from '../../../../../../../reusable/delete-button/DeleteButton';
import { Deletion } from '../../../../../../../reusable/deletion/Deletion';
import { Popup } from '../../../../../../../reusable/popup/Popup';

import { useReview } from '../../../../../../../../api/reviewApi';

import { useAuth } from '../../../../../../../../hooks/useAuth';

export const ReviewDeleteButton = ({ existingReview, onReviewDeleted, onError }) => {
    const { deleteReview } = useReview();
    const { isAuthenticated } = useAuth();

    const [isDeleting, setIsDeleting] = useState(false);
    const [isDeletePopupOpen, setIsDeletePopupOpen] = useState(false);

    const handleDelete = async () => {
        if (!existingReview || !isAuthenticated) {
            return;
        }

        setIsDeleting(true);
        setIsDeletePopupOpen(false);

        try {
            await deleteReview(existingReview.id);
            onReviewDeleted?.();
        } catch (err) {
            onError?.(err.message || 'Failed to delete review');
        } finally {
            setIsDeleting(false);
        }
    };

    if (!existingReview) {
        return null;
    }

    return (
        <>
            <DeleteButton
                entityName="review"
                callbackHandler={() => setIsDeletePopupOpen(true)}
                disabled={isDeleting}
            />
            {isDeletePopupOpen && (
                <Popup isOpen={isDeletePopupOpen} onClose={() => setIsDeletePopupOpen(false)}>
                    <Deletion
                        entityName="review"
                        onProceed={handleDelete}
                        onCancel={() => setIsDeletePopupOpen(false)}
                    />
                </Popup>
            )}
        </>
    );
};
