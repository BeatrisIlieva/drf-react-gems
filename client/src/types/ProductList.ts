export interface Product {
    id: number;
    collectionName: string;
    firstImage: string;
    secondImage: string;
    isSoldOut: boolean;
    colorName: string;
    stoneName: string;
    metalName: string;
    minPrice: string;
    maxPrice: string;
    averageRating: number;
}

export interface ProductsResponse {
    count: number;
    next: string | null;
    previous: string | null;
    results: Product[];
}

export interface FetchProductsParams {
    categoryName: string | undefined;
    page?: number | null;
    colorIds?: number[];
    stoneIds?: number[];
    metalIds?: number[];
    collectionIds?: number[];
    ordering?: string | null;
}

export interface FetchProductsParamsExtended extends FetchProductsParams {
    shouldUpdateProducts?: boolean;
    shouldSetProductsCount?: boolean;
    shouldResetOrdering?: boolean;
}
