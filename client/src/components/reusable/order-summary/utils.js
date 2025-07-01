import { formatPrice } from '../../../utils/formatPrice';

export const getTextRows = (shoppingBagTotalPrice) => {
    const price = formatPrice(shoppingBagTotalPrice.toString());

    const textRows = [
        {
            firstWord: 'Subtotal',
            firstWordImportance: 'highlighted',
            secondWord: `${price}`,
            secondWordImportance: 'highlighted'
        },
        {
            firstWord: 'Shipping',
            secondWord: 'Complimentary',
            secondWordImportance: 'subtle'
        },
        {
            firstWord: 'Total',
            firstWordImportance: 'highlighted',
            secondWord: `${price}`,
            secondWordImportance: 'highlighted',
            rowImportance: 'increased-font-size'
        }
    ];

    return textRows;
};
