import { useEffect, type ReactElement } from 'react';
import { useProductListContext } from '../../../contexts/ProductListContext';

import styles from './ProductList.module.scss';
import { ProductCard } from './product-card/ProductCard';
import { FilterList } from './filter-list/FilterList';
import { Button } from '../../reusable/button/Button';
import { HomeLink } from './home-link/HomeLink';
import { Nav } from './nav/Nav';
import { useSentinel } from '../../../hooks/useSentinel';
import { useCategoryName } from '../../../hooks/useCategoryName';

export const ProductList = (): ReactElement => {
    const { categoryName } = useCategoryName();
    const {
        products,
        // loading,
        // error,
        fetchProducts,
        loadMoreHandler,
        loadMoreDisabled,
        displayFilters,
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        orderingCriteria,
        page
    } = useProductListContext();

    const { sentinelRef, isSticky } = useSentinel();

    useEffect(() => {
        fetchProducts({
            categoryName,
            colorIds,
            stoneIds,
            metalIds,
            collectionIds,
            ordering: orderingCriteria,
            page
        });
    }, [
        fetchProducts,
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        orderingCriteria,
        page,
        categoryName
    ]);

    return (
        <section className={styles['product-list']}>
            <div ref={sentinelRef} className={styles['sentinel']} />

            <header className={isSticky ? styles['sticky'] : ''}>
                <HomeLink />
                <Nav />
            </header>
            <div
                className={`${styles['wrapper-products']} ${displayFilters ? styles['with-gap'] : styles['no-gap']}`}
            >
                <FilterList />

                <div className={styles['wrapper-inner']}>
                    <ul className={styles['products']}>
                        {products?.map((product) => (
                            <ProductCard key={product.id} {...product} />
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
