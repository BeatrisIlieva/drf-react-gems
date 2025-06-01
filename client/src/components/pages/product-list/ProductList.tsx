import { useEffect, type ReactElement } from 'react';
import { useProductListContext } from '../../../contexts/ProductListContext';

import styles from './ProductList.module.scss';
import { ProductCard } from './product-card/ProductCard';
import { useCategoryName } from '../../../hooks/useCategoryName';

export const ProductList = (): ReactElement => {
    const { data, loading, error, fetchProducts } =
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

    console.log(data);

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
                <div className={styles['filters']}>
                    <h3>filters</h3>
                </div>

                <ul className={styles['products']}>
                    {data?.results.map((product) => (
                        <ProductCard key={product.id} {...product} />
                    ))}
                </ul>
            </div>
        </section>
    );
};
