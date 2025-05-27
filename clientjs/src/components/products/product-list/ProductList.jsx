import { useProductListContext } from '../../../contexts/ProductListContext';
import styles from './ProductList.module.css';
import { ProductCard } from './product-card/ProductCard';
import { Filters } from './filters/Filters';
import { useState } from 'react';

export const ProductList = () => {
    const { categoryName, products, loadMore, loadMoreDisabled } = useProductListContext();
    const [displaySortBy, setDisplaySortBy] = useState(false);

    const toggleDisplaySortBy = () => {
        setDisplaySortBy(() => !displaySortBy);
    };

    return (
        <section className={styles['product-list']}>
            <header>
                <h2>{categoryName}</h2>
            </header>
            <nav className={styles['secondary']}>
                <ul>
                    <li>Filters</li>
                    <li onClick={toggleDisplaySortBy}>
                        <button>Sort By</button>
                        {displaySortBy && (
                            <span>
                                <button>Best Rating</button>
                                <button>Available Now</button>
                                <button>Price: Low to High</button>
                                <button>Price: High to Low</button>
                            </span>
                        )}
                    </li>
                </ul>
            </nav>
            <div>
                <Filters />
                <section>
                    <ul>
                        {products.map((product) => (
                            <ProductCard
                                key={product.id}
                                {...product}
                                category__name={categoryName}
                            />
                        ))}
                    </ul>
                    <button onClick={loadMore} disabled={loadMoreDisabled}>
                        Load More
                    </button>
                </section>
            </div>
        </section>
    );
};
