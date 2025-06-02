import { useEffect, type ReactElement } from 'react';
import { useProductListContext } from '../../../contexts/ProductListContext';

import styles from './ProductList.module.scss';
import { ProductCard } from './product-card/ProductCard';
import { FilterList } from './filter-list/FilterList';
import { Button } from '../../reusable/button/Button';
import { HomeLink } from './home-link/HomeLink';
import { Nav } from './nav/Nav';

export const ProductList = (): ReactElement => {
    const {
        products,
        loading,
        error,
        fetchProducts,
        loadMoreHandler,
        loadMoreDisabled,
        displayFilters
    } = useProductListContext();

    useEffect(() => {
        fetchProducts();
    }, [fetchProducts]);

    return (
        <section className={styles['product-list']}>
            <HomeLink />
            <Nav />
            <div
                className={`${styles['wrapper-products']} ${displayFilters ? styles['with-gap'] : styles['no-gap']}`}
            >
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
