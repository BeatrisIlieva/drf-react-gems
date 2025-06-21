export interface Color {
    name: string;
    id: number;
    count: number;
}

export interface Stone {
    name: string;
    id: number;
    count: number;
}

export interface Metal {
    name: string;
    id: number;
    count: number;
}

export interface Collection {
    name: string;
    id: number;
    count: number;
}

export interface FetchFiltersParams {
    categoryName: string | undefined;
    entityName: string | undefined;
    colorIds?: number[];
    stoneIds?: number[];
    metalIds?: number[];
    collectionIds?: number[];
}

export interface FiltersResponse {
    results: Color[] | Stone[] | Collection[] | Metal[];
}

export type EntityName = 'Collection' | 'Color' | 'Metal' | 'Stone';
