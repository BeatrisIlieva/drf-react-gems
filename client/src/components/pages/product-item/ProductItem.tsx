import { useEffect, useState, type ReactElement } from 'react';
import { useProductItem } from '../../../api/productItemApi';
import type { ProductItemType } from '../../../types/Products';
import { useParams } from 'react-router';

import styles from './ProductItem.module.scss';
import { Nav } from './nav/Nav';

export const ProductItem = (): ReactElement => {
    const { getProductItem } = useProductItem();
    const { categoryName, productId } = useParams<{
        categoryName: string;
        productId: string;
    }>();

    const [product, setProduct] = useState<ProductItemType | null>(null);

    useEffect(() => {
        getProductItem({ categoryName, productId })
            .then((response) => {
                setProduct(response.product);
            })
            .catch((error) => {
                console.error('Error fetching product item:', error);
            });
    }, [categoryName, productId, getProductItem]);
    

    return (
        <section className={styles['product-item']}>
            <Nav />
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
