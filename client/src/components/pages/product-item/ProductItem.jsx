import { UserAction } from '../../reusable/user-action/UserAction';
import { Nav } from './nav/Nav';
import { ProductImages } from './product-images/ProductImages';
import { RelatedProducts } from './related-products/RelatedProducts';
import { ReviewList } from './review-list/ReviewList';

import { useProductItemContext } from '../../../contexts/ProductItemContext';

import styles from './ProductItem.module.scss';

export const ProductItem = () => {
    const { loading, isTransitioning } = useProductItemContext();

    return (
        <>
            {!loading && (
                <section className={styles['product-item']}>
                    <div
                        className={
                            isTransitioning ? 'content-transition-out' : 'content-transition-in'
                        }
                    >
                        <Nav />
                        <div>
                            <ProductImages />
                            <ReviewList />
                        </div>
                        <UserAction />
                    </div>
                    <RelatedProducts />
                </section>
            )}
        </>
    );
};
