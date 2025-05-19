import { useState, useEffect, useCallback } from 'react';
import { useLocation } from 'react-router';
import { useProducts } from '../../../api/productsApi';

import styles from './ProductList.module.css';
import { ProductCard } from './product-card/ProductCard';
import { Filters } from './filters/Filters';

const initialFiltersData = {
    materials: { title: 'Material', elements: {} },
    prices: { title: 'Price', elements: {} },
    colors: { title: 'Color', elements: {} },
    stones: { title: 'Stone', elements: {} },
    categories: { title: 'Category', elements: {} },
    sizes: { title: 'Size', elements: {} },
    collections: { title: 'Collection', elements: {} }
};

export const ProductList = () => {
    const [categoryName, setCategoryName] = useState([]);
    const [categoryId, setCategoryId] = useState(null);
    const [products, setProducts] = useState([]);
    const [totalProductsCount, setTotalProductsCount] = useState(0);
    const [page, setPage] = useState(1);
    const location = useLocation();
    const { getProducts } = useProducts();
    const [loadMoreDisabled, setLoadMoreDisabled] = useState(false);
    const [filtersData, setFiltersData] = useState(initialFiltersData);

    const updateColorsData = useCallback((allProducts) => {
        const colorsData = {};

        allProducts.forEach((product) => {
            product.stones.forEach((stone) => {
                const color = stone.color;
                const hex = stone.hex;

                if (!colorsData[color]) {
                    colorsData[color] = { count: 0, hex };
                }

                colorsData[color].count += 1;
            });
        });

        setFiltersData((state) => ({
            ...state,
            colors: {
                ...state.colors,
                elements: colorsData
            }
        }));
    }, []);

    useEffect(() => {
        setLoadMoreDisabled(() => totalProductsCount <= products.length);
    }, [products, totalProductsCount, location]);

    useEffect(() => {
        const pathItems = location.pathname.split('/').splice(1);
        const itemName = pathItems[1];
        const itemId = pathItems[2];

        const nameCapitalized =
            itemName.charAt(0).toUpperCase() + itemName.slice(1) + 's';

        setCategoryName(nameCapitalized);
        setCategoryId(itemId);

        getProducts(itemId)
            .then((response) => {
                setProducts(response.results);
                setTotalProductsCount(response.count);
                updateColorsData(response.results);
            })
            .catch((err) => console.log(err.message));
    }, [location, getProducts, updateColorsData]);

    useEffect(() => {
        setPage(1);
    }, [location]);

    const loadMoreHandler = () => {
        if (totalProductsCount <= products.length) return;

        setPage((prev) => prev + 1);
    };

    useEffect(() => {
        if (page === 1) return;

        getProducts(categoryId, page)
            .then((response) => {
                setProducts((prev) => {
                    const updatedProducts = [...prev, ...response.results];
                    updateColorsData(updatedProducts); // pass full list here
                    return updatedProducts;
                });
            })
            .catch((err) => console.log(err.message));
    }, [page, categoryId, getProducts, updateColorsData]);

    return (
        <section className={styles['product-list']}>
            <header>
                <h2>{categoryName}</h2>
            </header>
            <nav className={styles['secondary']}>
                <ul>
                    <li>Filters</li>
                    <li>Sort By</li>
                </ul>
            </nav>
            <div>
                <Filters data={filtersData} />
                <section>
                    <ul>
                        {products.length > 0 &&
                            products.map((product) => (
                                <ProductCard key={product.id} {...product} />
                            ))}
                    </ul>
                    <button
                        onClick={loadMoreHandler}
                        disabled={loadMoreDisabled}
                    >
                        Load More
                    </button>
                </section>
            </div>
        </section>
    );
};
