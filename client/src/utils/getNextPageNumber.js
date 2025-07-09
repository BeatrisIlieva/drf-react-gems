export const getNextPageNumber = nextUrl => {
    if (!nextUrl) return null;

    try {
        const url = new URL(nextUrl);
        const page = url.searchParams.get('page');

        return page ? Number(page) : null;
    } catch {
        return null;
    }
};
