function toSnakeCase(str) {
    return str
        .replace(/([A-Z])/g, '_$1')
        .toLowerCase()
        .replace(/^_/, ''); // Remove leading underscore if present
}

export const keysToSnakeCase = (obj) => {
    if (Array.isArray(obj)) {
        return obj.map(keysToSnakeCase);
    } else if (obj !== null && typeof obj === 'object') {
        return Object.entries(obj).reduce((acc, [key, value]) => {
            acc[toSnakeCase(key)] = keysToSnakeCase(value);
            return acc;
        }, {});
    }
    return obj;
};
