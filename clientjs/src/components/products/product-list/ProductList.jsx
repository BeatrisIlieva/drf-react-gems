import { useState, useEffect } from 'react';
import { useLocation } from 'react-router';
import { useProducts } from '../../../api/productsApi';

import styles from './ProductList.module.css';

export const ProductList = () => {
    const [categoryName, setCategoryName] = useState([]);
    const [categoryId, setCategoryId] = useState(0);
    const [products, setProducts] = useState([]);
    const [totalProductsCount, setTotalProductsCount] = useState(0);
    const [page, setPage] = useState(1);
    const location = useLocation();
    const { getProducts } = useProducts();

    useEffect(() => {
        const pathItems = location.pathname.split('/').splice(1);
        const itemName = pathItems[1];
        const itemId = pathItems[2];

        const nameCapitalized =
            itemName.charAt(0).toUpperCase() + itemName.slice(1) + 's';

        setCategoryName(() => nameCapitalized);
        setCategoryId(() => itemId);
    }, [location]);

    useEffect(() => {
        getProducts(categoryId)
            .then((response) => {
                setProducts(response.results);
                setTotalProductsCount(response.count);
                console.log(response);
            })
            .catch((err) => console.log(err.message));
    }, [categoryId, getProducts]);

    console.log(products);

    // const loadMoreHandler = () => {
    //     if(totalProductsCount <= products.length){
    //         return;
    //     } else {
    //         setPage((page) => page + 1)

    //         getProducts(categoryId, page)
    //         .then((response) => {
    //             setProducts((state) => [...state, ...response.results]);
    //             console.log(products)
    //         })
    //         .catch((err) => console.log(err.message));
    //     }
    // }

    const loadMoreHandler = () => {
        if (totalProductsCount <= products.length) return;

        // Just update the page number
        setPage((prev) => prev + 1);
    };

    // Fetch when `page` changes (except initial page load)
    useEffect(() => {
        if (page === 1) return; // initial load already done in other useEffect

        getProducts(categoryId, page)
            .then((response) => {
                setProducts((prev) => [...prev, ...response.results]);
            })
            .catch((err) => console.log(err.message));
    }, [page, categoryId, getProducts]);

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
                                    <div className={styles['thumbnail']}>
                                        <img
                                            src={product.first_image.image_url}
                                            alt={`${product.collection} ${product.reference} ${product.category}`}
                                        />
                                    </div>
                                    {/* <p>{`${product.collection.name} ${product.reference.name} ${product.category.name}`}</p> */}
                                </li>
                            ))}
                    </ul>
                    <button onClick={loadMoreHandler}>Load More</button>
                </section>
            </div>
        </section>
    );
};
