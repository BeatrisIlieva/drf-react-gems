export const formatCardNumber = value => {
    const digits = value.replace(/\D/g, '');

    const formatted = digits.replace(/(\d{4})(?=\d)/g, '$1 ');

    return formatted.substring(0, 19);
};

export const formatExpiryDate = value => {
    const digits = value.replace(/\D/g, '');

    if (digits.length >= 2) {
        return `${digits.substring(0, 2)}/${digits.substring(2, 4)}`;
    }

    return digits;
};

export const formatCvv = value => {
    return value.replace(/\D/g, '').substring(0, 3);
};
