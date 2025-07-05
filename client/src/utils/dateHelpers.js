export const formatOrderDate = (dateString) => {
    const date = new Date(dateString);
    
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
};

export const formatShortOrderId = (orderGroup) => {
    return orderGroup.substring(0, 8).toUpperCase();
};
