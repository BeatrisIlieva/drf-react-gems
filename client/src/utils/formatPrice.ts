export const formatPrice = (price: string): string => {
    const splittedPrice = price.split('.')[0];
    const start = splittedPrice.slice(
        0,
        splittedPrice.length - 3
    );
    const middle = ',';
    const end = splittedPrice.slice(start.length);
    const formattedPrice = `$${start}${middle}${end}`;

    return formattedPrice;
};
