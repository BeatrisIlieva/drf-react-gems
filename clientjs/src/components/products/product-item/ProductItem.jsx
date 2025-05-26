import styles from './ProductItem.module.css';

import { useEffect, useState } from 'react';
import { useProducts } from '../../../api/productsApi';
import { useParams } from 'react-router';
import { Button } from '../../reusable/button/Button';
import { HeartIcon } from '../../reusable/heart-icon/HeartIcon';

export const ProductItem = () => {
    const [product, setProduct] = useState(null);
    const { categoryName, productId } = useParams();
    const { getProduct } = useProducts();

    useEffect(() => {
        getProduct({ categoryName, productId }).then((result) => setProduct(result));
    }, [categoryName, productId, getProduct]);

    const productCategory = categoryName.charAt(0).toUpperCase() + categoryName.slice(1);
    const productDescription = `${product?.stone_by_color.color.name} ${product?.stone_by_color.stone.name}s set in ${product?.material.name}`;

    return (
        <>
            {product && (
                <section className={styles['product-item']}>
                    <div className={styles['wrapper-left']}>
                        <div className={styles['thumbnail']}>
                            <img src={product.second_image} alt='' />
                        </div>
                        <div className={styles['thumbnail']}>
                            <img src={product.first_image} alt='' />
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
                            <ul>
                                {product.related_products.map((item) => (
                                    <li
                                        key={item.id}
                                        className={`${styles['thumbnail']} ${
                                            product.id === item.id ? styles['selected'] : ''
                                        }`.trim()}
                                    >
                                        <img src={item.first_image} alt='' />
                                    </li>
                                ))}
                            </ul>
                            <span>Size:</span>
                            <ul>
                                {product.inventory.map((item) => (
                                    <li key={item.size.id}>
                                        <span>{item.size.name}</span>
                                        <span>cm</span>
                                    </li>
                                ))}
                            </ul>
                            <div>
                                <Button title={'Add to Bag'} color={'black'} />
                                <Button title={<HeartIcon />} color={'black'} />
                            </div>
                        </div>

                        <div className={styles['wrapper-bottom']}>
                            <h2>Customer reviws</h2>
                        </div>
                    </div>
                </section>
            )}
        </>
    );
};
