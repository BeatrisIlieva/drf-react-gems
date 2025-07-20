export const createBagItem = (product, bagInput, categoryName) => {
    const inventory = product.inventory.find(inv => inv.id === bagInput.inventory);

    if (!inventory) throw new Error('Inventory item not found');

    const productInfo = {
        productId: product.id,
        collection: product.collection?.name || '',
        price: Number(inventory.price),
        firstImage: product.firstImage,
        availableQuantity: inventory.quantity,
        size: inventory.size?.name || '',
        metal: product.metal?.name || '',
        stone: product.stone?.name || '',
        color: product.color?.name || '',
        category: categoryName || '',
    };

    return {
        id: bagInput.inventory,
        quantity: bagInput.quantity,
        createdAt: new Date().toISOString(),
        productInfo,
        totalPrice: productInfo.price * bagInput.quantity,
    };
};
