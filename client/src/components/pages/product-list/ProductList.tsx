import { useEffect, type ReactElement } from 'react';
import { useProductListContext } from '../../../contexts/ProductListContext';

import styles from './ProductList.module.scss';
import { ProductCard } from './product-card/ProductCard';
import { useCategoryName } from '../../../hooks/useCategoryName';
import { FilterList } from './filter-list/FilterList';
import { Button } from '../../reusable/button/Button';

export const ProductList = (): ReactElement => {
    const {
        products,
        loading,
        error,
        fetchProducts,
        loadMoreHandler,
        loadMoreDisabled
    } = useProductListContext();

    const { categoryNameCapitalizedPlural } = useCategoryName();

    useEffect(() => {
        fetchProducts();
    }, [fetchProducts]);

    return (
        <section className={styles['product-list']}>
            <p>
                <span>Home</span>
                <span>/</span>
                <span>{categoryNameCapitalizedPlural}</span>
            </p>
            <h1>{categoryNameCapitalizedPlural}</h1>
            <div>
                <h5>images wrapper</h5>
            </div>
            <nav>
                <ul>
                    <li>filters</li>
                    <li>sort by</li>
                </ul>
            </nav>
            <div className={styles['wrapper-products']}>
                <FilterList />

                <div className={styles['wrapper-inner']}>
                    <ul className={styles['products']}>
                        {products?.map((product) => (
                            <ProductCard
                                key={product.id}
                                {...product}
                            />
                        ))}
                    </ul>
                    {!loadMoreDisabled && products.length > 0 && (
                        <Button
                            callbackHandler={loadMoreHandler}
                            title={'Load More'}
                            color={'white'}
                            disabled={loadMoreDisabled}
                        />
                    )}
                </div>
            </div>
        </section>
    );
};
