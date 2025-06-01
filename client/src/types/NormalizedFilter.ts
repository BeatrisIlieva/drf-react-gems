export interface NormalizedFilterItem {
    id: string | number;
    label: string;
    count: number;
    hex?: string;
    image?: string;
}

export interface NormalizedFilterGroup {
    key: string;
    label: string;
    data: NormalizedFilterItem[];
}
