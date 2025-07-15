import { formatPrice } from '../../../../utils/formatPrice';

import styles from './PriceDisplay.module.scss';

export const PriceDisplay = ({
    selectedInventoryItem,
    formattedMinPrice,
    formattedMaxPrice,
    isAddingToBag,
}) => {
    const priceClassName = [
        styles['price-display'],
        selectedInventoryItem ? styles['selected-price'] : '',
        isAddingToBag ? 'animate-pulse' : '',
    ]
        .filter(Boolean)
        .join(' ');

    return (
        <p className={priceClassName}>
            {selectedInventoryItem ? (
                <span>{formatPrice(selectedInventoryItem.price)}</span>
            ) : (
                <>
                    <span>{formattedMinPrice}</span>
                    <span>-</span>
                    <span>{formattedMaxPrice}</span>
                </>
            )}
        </p>
    );
};
