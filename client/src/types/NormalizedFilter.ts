export interface NormalizedFilterItem {
    id: string | number;
    label: string;
    count: number;
    hex?: string;
    image?: string;
}

export type FilterLabel = 'Collection' | 'Color' | 'Metal' | 'Price' | 'Stone';

export interface NormalizedFilterGroup {
    key: string;
    label: FilterLabel;
    data: NormalizedFilterItem[];
}
