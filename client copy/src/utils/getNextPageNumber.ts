export const getNextPageNumber = (nextUrl: string | null): number | null => {
    if (!nextUrl) return null;

    try {
        const url = new URL(nextUrl);
        const page = url.searchParams.get('page');

        return page ? Number(page) : null;
    } catch (err) {
        console.log(err);
        return null;
    }
};
