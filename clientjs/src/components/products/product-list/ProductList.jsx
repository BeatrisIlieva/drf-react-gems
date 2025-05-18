import { useState, useEffect } from 'react';
import { useLocation } from 'react-router';
import { useProducts } from '../../../api/productsApi';

import styles from './ProductList.module.css';

export const ProductList = () => {
    const [categoryName, setCategoryName] = useState([]);
    const [categoryId, setCategoryId] = useState(null);
    const [products, setProducts] = useState([]);
    const [totalProductsCount, setTotalProductsCount] = useState(0);
    const [page, setPage] = useState(1);
    const location = useLocation();
    const { getProducts } = useProducts();
    const [loadMoreDisabled, setLoadMoreDisabled] = useState(false);

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
            })
            .catch((err) => console.log(err.message));
    }, [location, getProducts]);

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
                setProducts((state) => [...state, ...response.results]);
            })
            .catch((err) => console.log(err.message));
    }, [page, categoryId, getProducts]);

    console.log(products);

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
                <aside>
                    <h4>Filtrations</h4>
                </aside>
                <section>
                    <ul>
                        {products.length > 0 &&
                            products.map((product) => (
                                <li key={product.id}>
                                    <span className={styles['thumbnail']}>
                                        <img
                                            src={product.first_image}
                                            // alt={`${product.collection} ${product.reference} ${product.category}`}
                                        />
                                    </span>
                                    <span className={styles['stones']}>
                                        {product.stones.map(item => (
                                            <span key={`${product.id}-${item.color}-${item.name}`}>
                                                <img src={item.image} alt="" />
                                            </span>
                                        ))}
                                    </span>
                                </li>
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
