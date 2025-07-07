import styles from './ProductItem.module.scss';
import { Nav } from './nav/Nav';
import { MainContent } from './main-content/MainContent';
import { RelatedProducts } from './related-products/RelatedProducts';
import { useProductItemContext } from '../../../contexts/ProductItemContext';
import { Skeleton } from './skeleton/Skeleton';

export const ProductItem = () => {
    const { loading, isTransitioning } = useProductItemContext();

    if (loading) {
        return <section className={styles['product-item']}></section>;
    }

    return (
        <section className={styles['product-item']}>
            <div className={isTransitioning ? 'content-transition-out' : 'content-transition-in'}>
                <Nav />
                <MainContent />
                <RelatedProducts />
            </div>
        </section>
    );
};
