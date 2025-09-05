import { LoadingSpinner } from '../../common/loading-spinner/LoadingSpinner';
import { Button } from '../../reusable/button/Button';
import { ProductItems } from '../../reusable/product-items/ProductItems';
import { FilterList } from './filter-list/FilterList';
import { HomeLink } from './home-link/HomeLink';
import { Nav } from './nav/Nav';

import { useSentinel } from '../../../hooks/useSentinel';

import { useProductFiltersContext } from '../../../contexts/ProductFiltersContext';
import { useProductListContext } from '../../../contexts/ProductListContext';

import styles from './ProductList.module.scss';

export const ProductList = () => {
    const { products, loading, loadMoreHandler, loadMoreDisabled } = useProductListContext();
    const { displayFilters } = useProductFiltersContext();

    const { sentinelRef, isSticky } = useSentinel();

    return (
        <>
            <section className={styles['product-list']}>
                <div ref={sentinelRef} className={styles['sentinel']} />

                <HomeLink />
                {!loading && (
                    <header className={isSticky ? styles['sticky'] : ''}>
                        <Nav />
                    </header>
                )}
                <div
                    className={`${styles['wrapper-products']} ${
                        displayFilters ? styles['with-gap'] : styles['no-gap']
                    }`}
                >
                    <FilterList />

                    {loading && <LoadingSpinner />}

                    <div className={styles['wrapper-inner']}>
                        {products.length > 0 && <ProductItems products={products} />}
                    </div>
                </div>
                {!loadMoreDisabled && (
                    <Button
                        color="black"
                        title="Load more"
                        buttonGrow="1"
                        width="10"
                        callbackHandler={loadMoreHandler}
                    />
                )}
            </section>
        </>
    );
};
