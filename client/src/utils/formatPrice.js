export const formatPrice = (price) => {
    // Handle null, undefined, or empty values
    if (!price && price !== 0) {
        return '$0';
    }
    
    // Convert to string if it's a number
    const priceStr = typeof price === 'number' ? price.toString() : price;
    
    // Handle decimal numbers
    const [wholePart, decimalPart] = priceStr.split('.');
    
    if (wholePart.length <= 3) {
        // If less than or equal to 3 digits, no comma needed
        return decimalPart ? `$${wholePart}.${decimalPart}` : `$${wholePart}`;
    }
    
    // Add comma for thousands
    const start = wholePart.slice(0, wholePart.length - 3);
    const end = wholePart.slice(start.length);
    const formattedWhole = `${start},${end}`;
    
    return decimalPart ? `$${formattedWhole}.${decimalPart}` : `$${formattedWhole}`;
};
