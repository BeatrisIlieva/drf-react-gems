export interface NormalizedFilterItem {
    id: number;
    label: string;
    count: number;
    hex?: string;
    image?: string;
}

export type FilterLabel = 'Collection' | 'Color' | 'Metal' | 'Stone';

export interface NormalizedFilterGroup {
    key: string;
    label: FilterLabel;
    data: NormalizedFilterItem[];
}
