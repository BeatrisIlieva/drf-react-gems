import { type ReactElement } from 'react';

import styles from './ProductItem.module.scss';
import { Nav } from './nav/Nav';
import { MainContent } from './main-content/MainContent';
import { RelatedProducts } from './related-products/RelatedProducts';

export const ProductItem = (): ReactElement => {
    return (
        <section className={styles['product-item']}>
            <Nav />
            <MainContent />
            <RelatedProducts
                relatedProducts={product.relatedProducts}
            />
        </section>
    );
};
