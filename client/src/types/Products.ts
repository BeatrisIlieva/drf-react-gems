export interface Color {
    name: string;
    id: number;
    count?: number;
}

export interface Stone {
    name: string;
    id: number;
    count?: number;
}

export interface Metal {
    name: string;
    id: number;
    count?: number;
}

export interface Collection {
    name: string;
    id: number;
    count?: number;
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

export type EntityName =
    | 'Collection'
    | 'Color'
    | 'Metal'
    | 'Stone';

export interface NormalizedFilterItem {
    id: number;
    label: string;
    count: number;
    hex?: string;
    image?: string;
}

export interface NormalizedFilterGroup {
    key: string;
    label: EntityName;
    data: NormalizedFilterItem[];
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

export interface FetchProductsParamsExtended
    extends FetchProductsParams {
    shouldUpdateProducts?: boolean;
    shouldSetProductsCount?: boolean;
    shouldResetOrdering?: boolean;
}

export interface FetchProductParams {
    categoryName: string | undefined;
    productId: string | undefined;
}

interface Size {
    id: number;
    name: string;
}

export interface InventoryItem {
    id: number;
    size: Size;
    quantity: number;
    price: string;
    contentType: string;
    objectId: number;
}

export interface Review {
    id: number;
    user: number;
    rating: number;
    comment: string;
    createdAt: string;
    contentType: number;
    objectId: number;
    photoUrl: string;
    userFullName: string;
}

interface BaseProduct {
    id: number;
    firstImage: string;
    secondImage: string;
    averageRating: number;
}

export interface ProductListType extends BaseProduct {
    collectionName: string;
    isSoldOut: boolean;
    colorName: string;
    stoneName: string;
    metalName: string;
    minPrice: string;
    maxPrice: string;
}

export interface ProductListResponse {
    count: number;
    next: string | null;
    previous: string | null;
    results: ProductListType[];
}

export interface RelatedProductType {
    id: number;
    firstImage: string;
    productType: string;
}

export interface ProductItemType extends BaseProduct {
    inventory: InventoryItem[];
    review: Review[];
    relatedCollectionProducts: ProductItemType[];
    relatedProducts: RelatedProductType[];
    createdAt: string;
    collection: Collection;
    color: Color;
    metal: Metal;
    stone: Stone;
}

export interface ProductItemResponse {
    product: ProductItemType;
}
