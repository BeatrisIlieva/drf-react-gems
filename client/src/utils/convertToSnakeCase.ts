function toSnakeCase(str: string): string {
    return str
        .replace(/([A-Z])/g, '_$1')
        .toLowerCase()
        .replace(/^_/, ''); // Remove leading underscore if present
}

export const keysToSnakeCase = (obj: unknown): unknown => {
    if (Array.isArray(obj)) {
        return obj.map(keysToSnakeCase);
    } else if (obj !== null && typeof obj === 'object') {
        return Object.entries(obj as Record<string, unknown>).reduce(
            (acc, [key, value]) => {
                acc[toSnakeCase(key)] = keysToSnakeCase(value);
                return acc;
            },
            {} as Record<string, unknown>
        );
    }
    return obj;
};
