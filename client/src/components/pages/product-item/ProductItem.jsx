import styles from './ProductItem.module.scss';
import { Nav } from './nav/Nav';
import { MainContent } from './main-content/MainContent';
import { RelatedProducts } from './related-products/RelatedProducts';
import { useProductItemContext } from '../../../contexts/ProductItemContext';
import { Skeleton } from './skeleton/Skeleton';

export const ProductItem = () => {
    const { loading } = useProductItemContext();

    return (
        <section className={styles['product-item']}>
            {loading ? (
                <Skeleton />
            ) : (
                <>
                    <Nav />
                    <MainContent />
                    <RelatedProducts />
                </>
            )}
        </section>
    );
};
