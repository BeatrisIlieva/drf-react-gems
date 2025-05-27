import styles from './ProductItem.module.css';

import { useEffect, useState } from 'react';
import { useProduct } from '../../../api/productsApi';
import { useParams } from 'react-router';
import { Button } from '../../reusable/button/Button';
import { HeartIcon } from '../../reusable/heart-icon/HeartIcon';
import { Reviews } from './reviews/Reviews';
import { TruckIcon } from '../../reusable/truck-icon/TruckIncon';
import { SizeList } from './size-list/SizeList';
import { useShoppingBag } from '../../../api/useShoppingBagApi';

export const ProductItem = () => {
    const [product, setProduct] = useState(null);
    const { categoryName, productId } = useParams();
    const { getProduct } = useProduct();
    const { addToBag } = useShoppingBag();

    const [selectedSize, setSelectedSize] = useState(null);
    const [selectedInventory, setSelectedInventory] = useState({});
    const [displayNotSelectedSizeErrorMessage, setDisplayNotSelectedSizeErrorMessage] =
        useState(false);

    const selectSizeClickHandler = (size) => {
        if (selectedSize === null) {
            setSelectedSize(size);
        } else if (selectedSize === size) {
            setSelectedSize(null);
            setSelectedInventory({});
        } else {
            setSelectedSize(size);
        }
    };

    const updateSelectedInventoryHandler = (contentType, objectId) => {
        setSelectedInventory({
            quantity: 1,
            contentType,
            objectId
        });
    };

    const addToBagHandler = () => {
        if (selectedSize === null) {
            setDisplayNotSelectedSizeErrorMessage(true);
        } else {
            addToBag(selectedInventory);
        }
    };

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
                            <img src={product.second_image} alt={productCategory} />
                        </div>
                        <div className={styles['thumbnail']}>
                            <img src={product.first_image} alt={productCategory} />
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

                            {categoryName !== 'earwear' && (
                                <SizeList
                                    sizes={product.inventory}
                                    selectedSize={selectedSize}
                                    clickHandler={selectSizeClickHandler}
                                    updateSelectedInventoryHandler={updateSelectedInventoryHandler}
                                    errorOccurred={displayNotSelectedSizeErrorMessage}
                                />
                            )}
                            <div>
                                <Button
                                    callbackHandler={addToBagHandler}
                                    title={'Add to Bag'}
                                    color={'black'}
                                    actionType={'button'}
                                />
                                <Button
                                    title={<HeartIcon />}
                                    color={'black'}
                                    actionType={'button'}
                                />
                            </div>
                        </div>

                        <p>
                            <TruckIcon />
                            <span>Complimentary 2-day shipping</span>
                        </p>

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
