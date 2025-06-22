import { useEffect, useState, type ReactElement } from 'react';
import { useProductItem } from '../../../../api/productItemApi';
import { useParams } from 'react-router';
import type { ProductItemType } from '../../../../types/Products';

import styles from './MainContent.module.scss';
import { ProductDetails } from './product-details/ProductDetails';
import { UserAction } from './user-action/UserAction';

export const MainContent = (): ReactElement => {


    return (
        <>
            {product && (
                <section className={styles['main-content']}>
                    <ProductDetails
                        firstImage={product.firstImage}
                        secondImage={product.secondImage}
                        averageRating={product.averageRating}
                        reviews={product.review}
                    />
                    <UserAction
                        productId={product.id}
                        collectionName={product.collection.name}
                        colorName={product.color.name}
                        stoneName={product.stone.name}
                        metalName={product.metal.name}
                        inventory={product.inventory}
                        relatedProducts={
                            product.relatedCollectionProducts
                        }
                        firstImage={product.firstImage}
                    />
                </section>
            )}
        </>
    );
};
