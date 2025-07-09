import styles from "./ProductItem.module.scss";
import { Nav } from "./nav/Nav";
import { MainContent } from "./main-content/MainContent";
import { RelatedProducts } from "./related-products/RelatedProducts";
import { useProductItemContext } from "../../../contexts/ProductItemContext";

export const ProductItem = () => {
    const { loading, isTransitioning } = useProductItemContext();

    return (
        <>
            {!loading && (
                <section className={styles["product-item"]}>
                    <div
                        className={
                            isTransitioning
                                ? "content-transition-out"
                                : "content-transition-in"
                        }
                    >
                        <Nav />
                        <MainContent />
                        <RelatedProducts />
                    </div>
                </section>
            )}
        </>
    );
};
