import { type ReactElement } from 'react';

import styles from './ProductItem.module.scss';
import { Nav } from './nav/Nav';
import { MainContent } from './main-content/MainContent';
import { RelatedProducts } from './related-products/RelatedProducts';
import { useProductItemContext } from '../../../contexts/ProductItemContext';

export const ProductItem = (): ReactElement => {
    const { loading } = useProductItemContext();

    return (
        <>
            {!loading && (
                <section className={styles['product-item']}>
                    <Nav />
                    <MainContent />
                    <RelatedProducts />
                </section>
            )}
        </>
    );
};
