export interface Product {
    id: number;
    collectionName: string;
    firstImage: string;
    secondImage: string;
    isSoldOut: boolean;
    min: string;
    max: string;
}

interface Color {
    colorName: string;
    colorId: number;
    colorHexCode: string;
    colorCount: number;
}

interface Stone {
    stoneName: string;
    stoneId: number;
    stoneImage: string;
    stoneCount: number;
}

interface Metal {
    metalName: string;
    metalId: number;
    metalCount: number;
}

interface Collection {
    collectionName: string;
    collectionId: number;
    collectionCount: number;
}

interface PriceRange {
    priceRange: string;
    count: number;
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
    prices: PriceRange[];
}

export interface FetchProductsParams {
    categoryName: string;
    pageNumber?: string | null;
    colorIds?: string[];
    stoneIds?: string[];
    materialIds?: string[];
    collectionIds?: string[];
    prices?: string[];
}
