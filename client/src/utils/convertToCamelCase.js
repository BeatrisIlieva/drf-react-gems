function toCamelCase(str) {
    return str
        .replace(/__([a-z])/g, (_, c) => c.toUpperCase())
        .replace(/_([a-z])/g, (_, c) => c.toUpperCase());
}

export const keysToCamelCase = obj => {
    if (Array.isArray(obj)) {
        return obj.map(keysToCamelCase);
    } else if (obj !== null && typeof obj === 'object') {
        return Object.entries(obj).reduce((acc, [key, value]) => {
            acc[toCamelCase(key)] = keysToCamelCase(value);
            return acc;
        }, {});
    }
    return obj;
};
