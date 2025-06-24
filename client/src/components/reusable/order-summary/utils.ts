import { formatPrice } from '../../../utils/formatPrice';

interface TextRow {
    firstWord: string;
    firstWordImportance?: 'highlighted' | string;
    secondWord: string;
    secondWordImportance?: 'highlighted' | 'subtle' | string;
    rowImportance?: 'increased-font-size' | string;
}

export const getTextRows = (
    shoppingBagTotalPrice: number
): TextRow[] => {
    const price = formatPrice(shoppingBagTotalPrice.toString());

    const textRows: TextRow[] = [
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
