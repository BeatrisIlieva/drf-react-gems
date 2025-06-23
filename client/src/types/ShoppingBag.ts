export interface CreateShoppingBagParams {
    contentType: string;
    objectId: number;
    quantity: number;
}

export interface UpdateShoppingBagParams extends CreateShoppingBagParams {
    id: number;  // Shopping bag item ID
}

export interface ProductInfo {
    productId: number;
    collection: string;
    price: number;
    firstImage: string;
    availableQuantity: number;
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
    createdAt: string;
    contentType: string;
    objectId: number;
    productInfo: ProductInfo;
    totalPricePerProduct: number;
}
