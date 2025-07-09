export const formatPrice = (price) => {
    if (!price && price !== 0) {
        return "$0";
    }

    const priceStr = typeof price === "number" ? price.toString() : price;

    const [wholePart, decimalPart] = priceStr.split(".");

    if (wholePart.length <= 3) {
        return decimalPart ? `$${wholePart}.${decimalPart}` : `$${wholePart}`;
    }

    const start = wholePart.slice(0, wholePart.length - 3);
    const end = wholePart.slice(start.length);
    const formattedWhole = `${start},${end}`;

    return decimalPart
        ? `$${formattedWhole}.${decimalPart}`
        : `$${formattedWhole}`;
};
