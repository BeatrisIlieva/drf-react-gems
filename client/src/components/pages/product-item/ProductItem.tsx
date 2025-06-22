import { useEffect, useState, type ReactElement } from 'react';
import { useProductItem } from '../../../api/productItemApi';
import type { ProductItemType } from '../../../types/Products';
import { useParams } from 'react-router';

import styles from './ProductItem.module.scss';
import { Nav } from './nav/Nav';
import { MainContent } from './main-content/MainContent';

export const ProductItem = (): ReactElement => {

    

    return (
        <section className={styles['product-item']}>
            <Nav />
            <MainContent />
            <section>
                <section>
                    <section>
                        <div>image</div>
                        <div>image</div>
                    </section>
                    <section>reviews</section>
                </section>
                <section>
                    add to shopping bag
                </section>
            </section>
            <section>related products</section>
        </section>
    )
};
