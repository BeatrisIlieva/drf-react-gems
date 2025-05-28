import styles from './ProductItem.module.css';
import { Reviews } from './reviews/Reviews';
import { SizeList } from './size-list/SizeList';
import { useProductItemContext } from '../../../contexts/ProductItemContext';
import { RelatedProductsList } from './related-products-list/RelatedProductsList';
import { UserAction } from './user-action/UserAction';
import { ComplimentaryShipping } from '../../reusable/complimentary-shipping/ComplimentaryShipping';

export const ProductItem = () => {
    const { product, productCategory, productDescription, categoryName } =
        useProductItemContext();

    return (
        <>
            {product && (
                <section className={styles['product-item']}>
                    <div className={styles['wrapper-left']}>
                        <div className={styles['thumbnail']}>
                            <img
                                src={product.second_image}
                                alt={productCategory}
                            />
                        </div>
                        <div className={styles['thumbnail']}>
                            <img
                                src={product.first_image}
                                alt={productCategory}
                            />
                        </div>
                    </div>

                    <div className={styles['wrapper-right']}>
                        <div className={styles['wrapper-top']}>
                            <h2>
                                <span>{product.collection.name}</span>
                                <sup>®</sup>
                                <span>{product.reference.name}</span>
                                <span>{productCategory}</span>
                            </h2>

                            <p>{productDescription}</p>

                            <span>{`$${product.price}`}</span>

                            <RelatedProductsList />

                            {categoryName !== 'earwear' && <SizeList />}

                            <UserAction />

                            <ComplimentaryShipping />
                        </div>

                        <div className={styles['wrapper-bottom']}>
                            <Reviews
                                reviews={product.reviews}
                                average_rating={product.average_rating}
                            />
                        </div>
                    </div>
                </section>
            )}
        </>
    );
};
