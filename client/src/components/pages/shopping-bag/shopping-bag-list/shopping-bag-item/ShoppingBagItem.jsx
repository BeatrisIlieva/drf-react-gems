import { useCallback, useState } from "react";
import styles from "./ShoppingBagItem.module.scss";

import { useShoppingBagContext } from "../../../../../contexts/ShoppingBagContext";
import { useWishlistContext } from "../../../../../contexts/WishlistContext";
import { QuantitySelector } from "./quantity-selector/QuantitySelector";
import { formatPrice } from "../../../../../utils/formatPrice";
import { useNavigate } from "react-router";

export const ShoppingBagItem = ({
    quantity,
    totalPrice,
    productInfo,
    id,
    contentType,
    objectId,
}) => {
    const { deleteShoppingBagHandler, isDeleting } = useShoppingBagContext();
    const { addToWishlist, isInWishlist } = useWishlistContext();
    const [isMovingToWishlist, setIsMovingToWishlist] = useState(false);
    const navigate = useNavigate();

    const category = productInfo.category?.toLowerCase();
    const productId = productInfo.productId;
    const isItemInWishlist = isInWishlist(category, productId);
    const formattedTotalPricePerProduct = formatPrice(totalPrice.toString());

    const moveToWishListHandler = async () => {
        if (isMovingToWishlist || isDeleting || isItemInWishlist) return;

        setIsMovingToWishlist(true);
        try {
            const categoryValue = category.endsWith("s")
                ? category.slice(0, -1)
                : category;

            const success = await addToWishlist(categoryValue, productId);
            if (success) {
                await deleteShoppingBagHandler(id);
            }
        } catch (error) {
            console.error("Error moving item to wishlist:", error);
        } finally {
            setIsMovingToWishlist(false);
        }
    };

    const navigateToProductItem = useCallback(() => {
        navigate(
            `/products/${
                productInfo.category.toLowerCase() + "s"
            }/${productInfo.productId}`,
        );
    }, [navigate, productInfo.category, productInfo.productId]);

    return (
        <li className={styles["shopping-bag-item"]}>
            <span
                className={styles["thumbnail"]}
                onClick={navigateToProductItem}
            >
                <img
                    src={productInfo.firstImage}
                    alt={productInfo.collection}
                />
            </span>

            <span>
                <span>
                    <span>{`${productInfo.collection} ${productInfo.category}`}</span>

                    <span>
                        {`${productInfo.color} ${productInfo.stone} set in ${productInfo.metal}`}
                    </span>

                    <span>
                        <span>Size: {productInfo.size}</span>
                    </span>
                </span>

                <span>
                    <button
                        onClick={moveToWishListHandler}
                        disabled={
                            isDeleting || isMovingToWishlist || isItemInWishlist
                        }
                        className={
                            isItemInWishlist
                                ? styles["in-wishlist"]
                                : isDeleting || isMovingToWishlist
                                  ? styles["removing"]
                                  : ""
                        }
                    >
                        {isMovingToWishlist
                            ? "Moving..."
                            : isItemInWishlist
                              ? "In Wishlist"
                              : "Move to Wish List"}
                    </button>
                    <button
                        onClick={() => {
                            deleteShoppingBagHandler(id);
                        }}
                        disabled={isDeleting}
                        className={isDeleting ? styles["removing"] : ""}
                    >
                        {isDeleting ? "Removing..." : "Remove"}
                    </button>
                </span>
            </span>

            <span>
                <span>{`${formattedTotalPricePerProduct}`}</span>
                <QuantitySelector
                    quantity={quantity}
                    id={id}
                    contentType={contentType}
                    objectId={objectId}
                    availableQuantity={productInfo.availableQuantity}
                />
            </span>
        </li>
    );
};
