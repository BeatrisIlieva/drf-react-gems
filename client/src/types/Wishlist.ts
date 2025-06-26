export interface WishlistItem {
    id: number;
    user: number | null;
    guest_id: string | null;
    created_at: string;
    content_type: string;
    object_id: number;
    product_info: {
        id: number;
        first_image: string;
        second_image: string;
        collection: string;
        color: string;
        metal: string;
        stone: string;
        product_type: string;
    } | null;
}

export interface WishlistCreateRequest {
    content_type: string;
    object_id: number;
}

export interface WishlistDeleteParams {
    content_type: string;
    object_id: number;
}

export interface WishlistResponse {
    results: WishlistItem[];
    count: number;
}