import { useEffect, type ReactElement } from 'react';
import { useProductListContext } from '../../../contexts/ProductListContext';

import styles from './ProductList.module.scss';
import { ProductCard } from './product-card/ProductCard';
import { useCategoryName } from '../../../hooks/useCategoryName';
import { FilterList } from './filter-list/FilterList';

export const ProductList = (): ReactElement => {
    const { products, loading, error, fetchProducts } =
        useProductListContext();
    const { categoryName, categoryNameCapitalizedPlural } =
        useCategoryName();

    useEffect(() => {
        if (categoryName) {
            fetchProducts({ categoryName, pageNumber: '1' });
        }
    }, [fetchProducts, categoryName]);

    if (loading) return <p>Loading products...</p>;
    if (error) return <p>Error: {error}</p>;

    console.log(products);

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
            <div className={styles['products-wrapper']}>
                <FilterList />

                <ul className={styles['products']}>
                    {products?.map((product) => (
                        <ProductCard key={product.id} {...product} />
                    ))}
                </ul>
            </div>
        </section>
    );
};
