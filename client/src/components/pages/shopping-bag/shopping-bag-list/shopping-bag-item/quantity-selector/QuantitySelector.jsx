import { useEffect, useState } from 'react';
import styles from './QuantitySelector.module.scss';
import { Icon } from '../../../../../reusable/icon/Icon';

import { useShoppingBagContext } from '../../../../../../contexts/ShoppingBagContext';
import { useShoppingBag } from '../../../../../../api/shoppingBagApi';

export const QuantitySelector = ({
    quantity,
    id,
    objectId,
    contentType,
    availableQuantity
}) => {
    const { updateItem } = useShoppingBag();
    const { refreshShoppingBag } = useShoppingBagContext();
    const [isUpdating, setIsUpdating] = useState(false);
    const [localQuantity, setLocalQuantity] = useState(quantity);

    const totalAvailableQuantity =
        typeof availableQuantity === 'string'
            ? parseInt(availableQuantity, 10) + quantity
            : availableQuantity + quantity;

    useEffect(() => {
        setLocalQuantity(quantity);
    }, [quantity]);

    const handleQuantityChange = async (newQuantity) => {
        if (newQuantity === localQuantity) return;

        setIsUpdating(true);
        try {
            await updateItem({
                contentType,
                objectId,
                quantity: newQuantity,
                id
            });
            setLocalQuantity(newQuantity);

            refreshShoppingBag();
        } catch (err) {
            console(err.message);
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
            setTimeout(() => {
                refreshShoppingBag();
            }, 100);
        }
    };

    return (
        <span className={styles['quantity-selector']}>
            <button
                onClick={decrementQuantity}
                disabled={isUpdating}
            >
                <Icon name='minus' />
            </button>
            <span>{localQuantity}</span>
            <button
                onClick={incrementQuantity}
                disabled={
                    isUpdating ||
                    localQuantity >= totalAvailableQuantity
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
