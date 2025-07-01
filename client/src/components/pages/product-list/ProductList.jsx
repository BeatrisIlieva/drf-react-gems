import { useCallback, useEffect } from 'react';
import { useProductListContext } from '../../../contexts/ProductListContext';

import styles from './ProductList.module.scss';

import { HomeLink } from './home-link/HomeLink';

import { useSentinel } from '../../../hooks/useSentinel';
import { useProductFiltersContext } from '../../../contexts/ProductFiltersContext';
import { Skeleton } from './skeleton/Skeleton';
import { Items } from './items/Items';
import { FilterList } from './filter-list/FilterList';
import { Nav } from './nav/Nav';

const SCROLL_OFFSET = 10;

function debounce(fn, delay) {
    let timeoutId;
    return () => {
        clearTimeout(timeoutId);
        timeoutId = window.setTimeout(fn, delay);
    };
}

export const ProductList = () => {
    const {
        products,
        loading,
        loadMoreHandler,
        loadMoreDisabled
    } = useProductListContext();
    const { displayFilters } = useProductFiltersContext();

    const { sentinelRef, isSticky } = useSentinel();

    const handleScroll = useCallback(() => {
        const scrollPosition =
            window.innerHeight + window.scrollY;
        const bottomPosition =
            document.documentElement.scrollHeight;

        const nearBottom =
            bottomPosition - scrollPosition < SCROLL_OFFSET;

        if (nearBottom && !loading && !loadMoreDisabled) {
            loadMoreHandler();
        }
    }, [loading, loadMoreDisabled, loadMoreHandler]);

    useEffect(() => {
        const debouncedScroll = debounce(handleScroll, 150);
        window.addEventListener('scroll', debouncedScroll);
        return () =>
            window.removeEventListener('scroll', debouncedScroll);
    }, [handleScroll]);

    return (
        <section className={styles['product-list']}>
            <div
                ref={sentinelRef}
                className={styles['sentinel']}
            />

            <HomeLink />

            <header className={isSticky ? styles['sticky'] : ''}>
                <Nav />
            </header>

            <div
                className={`${styles['wrapper-products']} ${
                    displayFilters
                        ? styles['with-gap']
                        : styles['no-gap']
                }`}
            >
                <FilterList />

                <div className={styles['wrapper-inner']}>
                    {loading &&
                    (!products || products.length === 0) ? (
                        <Skeleton />
                    ) : (
                        <Items />
                    )}
                </div>
            </div>
        </section>
    );
};
