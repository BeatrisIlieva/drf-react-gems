export const toggleIdInArray = (arr, id) =>
    arr.includes(id) ? arr.filter((i) => i !== id) : [...arr, id];
