export const toggleIdInArray = (arr: number[], id: number) =>
    arr.includes(id) ? arr.filter((i) => i !== id) : [...arr, id];
