export interface Product {
    id: number;
    collectionName: string;
    firstImage: string;
    secondImage: string;
    isSoldOut: boolean;
    colorName: string;
    stoneName: string;
    metalName: string;
    min: string;
    max: string;
    averageRating: number;
}

export interface Color {
    colorName: string;
    colorId: number;
    colorHexCode: string;
    colorCount: number;
}

export interface Stone {
    stoneName: string;
    stoneId: number;
    stoneImage: string;
    stoneCount: number;
}

export interface Metal {
    metalName: string;
    metalId: number;
    metalCount: number;
}

export interface Collection {
    collectionName: string;
    collectionId: number;
    collectionCount: number;
}

export interface ProductsResponse {
    count: number;
    next: string | null;
    previous: string | null;
    results: Product[];
    colors: Color[];
    stones: Stone[];
    metals: Metal[];
    collections: Collection[];
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
    shouldUpdateFiltersByEntity?: boolean;
    shouldResetFilters?: boolean;
    shouldSetProductsCount?: boolean;
    shouldResetOrdering?: boolean;
}

export type EntityName = 'Collection' | 'Color' | 'Metal' | 'Stone';
