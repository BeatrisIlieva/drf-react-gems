export const getTextRows = (shoppingBagTotalPrice) => {
    const textRows = [
        {
            firstWord: 'Subtotal',
            firstWordImportance: 'highlighted',
            secondWord: `$${shoppingBagTotalPrice}`,
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
            secondWord: `$${shoppingBagTotalPrice}`,
            secondWordImportance: 'highlighted',
            rowImportance: 'increased-font-size'
        }
    ];

    return textRows;
};
