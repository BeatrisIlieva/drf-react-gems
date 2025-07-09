import styles from "./UserAction.module.scss";
import { useCategoryName } from "../../../../../hooks/useCategoryName";
import { StyledTextBlock } from "../../../../reusable/styled-text-block/StyledTextBlock";
import { formatPrice } from "../../../../../utils/formatPrice";
import { RelatedProducts } from "./related-products/RelatedProducts";
import { SizeList } from "./size-list/SizeList";
import { Button } from "../../../../reusable/button/Button";
import { Icon } from "../../../../reusable/icon/Icon";
import { useProductItemContext } from "../../../../../contexts/ProductItemContext";
import { ComplimentaryShipping } from "../../../../reusable/complimentary-shipping/ComplimentaryShipping";
import { useWishlistContext } from "../../../../../contexts/WishlistContext";
import { Popup } from "../../../../reusable/popup/Popup";
import { useShoppingBagContext } from "../../../../../contexts/ShoppingBagContext";
import { ShoppingBagItem } from "../../../shopping-bag/shopping-bag-list/shopping-bag-item/ShoppingBagItem";
import { useNavigate } from "react-router";

export const UserAction = () => {
    const { categoryNameCapitalizedSingular, categoryName } = useCategoryName();
    const { isInWishlist, handleWishlistToggle } = useWishlistContext();
    const navigate = useNavigate();
    const {
        collectionName,
        colorName,
        stoneName,
        metalName,
        inventory,
        createShoppingBagHandler,
        notSelectedSizeError,
        isSoldOut,
        isAddingToBag,
        productId,
        toggleMiniBagPopupOpen,
        isMiniBagPopupOpen,
        selectedSize,
    } = useProductItemContext();

    const { shoppingBagItems, shoppingBagItemsCount, shoppingBagTotalPrice } =
        useShoppingBagContext();

    const selectedInventoryItem = selectedSize
        ? inventory.find((item) => item.size.id === selectedSize)
        : null;

    const prices = inventory.map((item) => parseFloat(item.price));

    const formattedMinPrice = formatPrice(Math.min(...prices).toString());
    const formattedMaxPrice = formatPrice(Math.max(...prices).toString());

    const category = categoryName?.slice(0, categoryName?.length - 1);
    const isItemInWishlist = isInWishlist(category, productId);

    const navigateToCheckout = () => {
        navigate(`/user/checkout`);
    };

    const navigateToShoppingBag = () => {
        navigate(`/user/shopping-bag`);
    };

    return (
        <section
            className={`${styles["user-action"]} ${
                isAddingToBag
                    ? "animate-fade-out duration-300ms"
                    : "animate-fade-in duration-500ms"
            }`}
        >
            <h1>
                <span>{collectionName}</span>
                <span>{categoryNameCapitalizedSingular}</span>
            </h1>
            <StyledTextBlock
                text={`${colorName} ${stoneName} set in ${metalName}`}
                isSubtle={true}
            />
            <p
                className={`${styles["price-display"]} ${selectedInventoryItem ? styles["selected-price"] : ""} ${isAddingToBag ? "animate-pulse" : ""}`}
            >
                {selectedInventoryItem ? (
                    <span>{formatPrice(selectedInventoryItem.price)}</span>
                ) : (
                    <>
                        <span>{formattedMinPrice}</span>
                        <span>-</span>
                        <span>{formattedMaxPrice}</span>
                    </>
                )}
            </p>
            <RelatedProducts />
            <p
                className={`${
                    notSelectedSizeError ? styles["error"] : ""
                } ${isAddingToBag ? "animate-pulse" : ""}`.trim()}
            >
                Size:
            </p>
            <SizeList />
            <p
                className={`${
                    notSelectedSizeError ? styles["error"] : styles["invisible"]
                }`.trim()}
            >
                Please select a size.
            </p>

            <div className={styles["buttons-wrapper"]}>
                <Button
                    title={
                        isAddingToBag
                            ? "Adding..."
                            : isSoldOut
                              ? "Sold Out"
                              : "Add to Bag"
                    }
                    color={isSoldOut ? "grey" : "black"}
                    callbackHandler={createShoppingBagHandler}
                    actionType={"button"}
                    disabled={isSoldOut || isAddingToBag}
                    buttonGrow="1"
                    className={isAddingToBag ? "animate-pulse" : ""}
                />
                <Button
                    title={
                        <Icon
                            name={isItemInWishlist ? "heart-filled" : "heart"}
                        />
                    }
                    color={"black"}
                    actionType={"button"}
                    callbackHandler={() =>
                        handleWishlistToggle(category + "s", productId)
                    }
                />
            </div>
            <ComplimentaryShipping />
            <Popup isOpen={isMiniBagPopupOpen} onClose={toggleMiniBagPopupOpen}>
                <div className={styles["mini-bag-header"]}>
                    <h3>Your Bag</h3>
                    <span>
                        {shoppingBagItemsCount}{" "}
                        {shoppingBagItemsCount > 1 ? "items" : "item"}
                    </span>
                </div>

                <ul className={styles["shopping-bag-list"]}>
                    {shoppingBagItems.map((item) => (
                        <ShoppingBagItem key={item.id} {...item} />
                    ))}
                </ul>
                <div className={styles["total-price-wrapper"]}>
                    <span>Total</span>
                    <span>{formatPrice(shoppingBagTotalPrice)}</span>
                </div>
                <div className={styles["mini-bag-buttons-wrapper"]}>
                    <Button
                        title="View Bag"
                        color="white"
                        buttonGrow="1"
                        callbackHandler={navigateToShoppingBag}
                    />
                    <Button
                        title="Continue Checkout"
                        color="black"
                        buttonGrow="1"
                        callbackHandler={navigateToCheckout}
                    />
                </div>
            </Popup>
        </section>
    );
};
