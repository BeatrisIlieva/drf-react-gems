import { useEffect, useRef, useState, type ReactElement } from 'react';
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

    const sentinelRef = useRef<HTMLDivElement>(null);
    const [isSticky, setIsSticky] = useState(false);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                setIsSticky(!entry.isIntersecting);
            },
            {
                root: null,
                threshold: 0,
            }
        );

        const sentinel = sentinelRef.current;
        if (sentinel) {
            observer.observe(sentinel);
        }

        return () => {
            if (sentinel) {
                observer.unobserve(sentinel);
            }
        };
    }, []);



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
