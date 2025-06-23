export interface AddToBagParams {
    contentType: string;
    objectId: number;
    quantity: number;
}

export interface ProductInfo {
    product_id: number;
    collection: string;
    price: number;
    first_image: string;
    available_quantity: number;
    size: string;
    metal: string;
    stone: string;
    color: string;
    category: string;
}

export interface ShoppingBagItemResponse {
    id: number;
    user: string | null;
    quantity: number;
    created_at: string; // ISO date string format
    content_type: string;
    object_id: number;
    product_info: ProductInfo;
    total_price_per_product: number;
}
