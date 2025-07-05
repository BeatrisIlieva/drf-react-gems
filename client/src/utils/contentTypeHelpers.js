// Maps product category names to Django content type model names
export const getContentTypeFromCategory = (category) => {
    if (!category) return null;

    const categoryMap = {
        earwear: 'earwear',
        fingerwear: 'fingerwear',
        neckwear: 'neckwear',
        wristwear: 'wristwear'
    };

    return (
        categoryMap[category.toLowerCase()] ||
        category.toLowerCase()
    );
};

// Maps product type to appropriate content type
export const getContentTypeFromProductType = (productType) => {
    if (!productType) return null;

    // Handle both singular and plural forms
    const typeMap = {
        earwear: 'earwear',
        earwears: 'earwear',
        fingerwear: 'fingerwear',
        fingerwears: 'fingerwear',
        neckwear: 'neckwear',
        neckwears: 'neckwear',
        wristwear: 'wristwear',
        wristwears: 'wristwear'
    };

    return (
        typeMap[productType.toLowerCase()] ||
        productType.toLowerCase()
    );
};
