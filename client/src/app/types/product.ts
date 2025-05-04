export interface PaginatedProducts {
    count: number;
    next: string | null;
    previous: string | null;
    results: Product[];
}

export interface Product {
    id: number;
    first_image: string;
    second_image: string;
    category: number;
    collection: number;
    material: number;
    reference: number;
    stones_colors: number[];
}
