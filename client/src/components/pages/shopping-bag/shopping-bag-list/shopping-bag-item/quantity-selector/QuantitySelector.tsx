import { useEffect, useState, type ReactElement } from 'react';
import styles from './QuantitySelector.module.scss';
import { Icon } from '../../../../../reusable/icon/Icon';
import { useUpdateShoppingBag } from '../../../../../../api/shoppingBagApi';

interface Props {
    quantity: number;
    id: number;
    objectId: number;
    contentType: string;
    availableQuantity: number;
}

export const QuantitySelector = ({
    quantity,
    id,
    objectId,
    contentType,
    availableQuantity
}: Props): ReactElement => {
    const { updateShoppingBag } = useUpdateShoppingBag();
    const [isUpdating, setIsUpdating] = useState(false);
    const [localQuantity, setLocalQuantity] = useState(quantity);

    useEffect(() => {
        setLocalQuantity(quantity);
    }, [quantity]);

    const handleQuantityChange = async (newQuantity: number) => {
        if (newQuantity === localQuantity) return;

        setIsUpdating(true);
        try {
            await updateShoppingBag({
                contentType,
                objectId,
                quantity: newQuantity,
                id
            });
            setLocalQuantity(newQuantity);
        } catch (error) {
            console.error('Error updating quantity:', error);

            setLocalQuantity(quantity);
        } finally {
            setIsUpdating(false);
        }
    };

    const incrementQuantity = () => {
        handleQuantityChange(localQuantity + 1);
    };

    const decrementQuantity = () => {
        if (localQuantity > 1) {
            handleQuantityChange(localQuantity - 1);
        } else {
            handleQuantityChange(0);
        }
    };

    return (
        <span className={styles['quantity-selector']}>
            <button
                onClick={decrementQuantity}
                disabled={isUpdating || availableQuantity === 0}
            >
                <Icon name='minus' />
            </button>
            <span>{localQuantity}</span>
            <button
                onClick={incrementQuantity}
                disabled={
                    isUpdating ||
                    localQuantity === availableQuantity
                }
            >
                <Icon name='plus' />
            </button>
            {isUpdating && (
                <span className={styles['updating-indicator']}>
                    Updating...
                </span>
            )}
        </span>
    );
};
