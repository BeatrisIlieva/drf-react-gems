import { useProductContext } from '../../../contexts/ProductContext';
import styles from './ProductList.module.css';
import { ProductCard } from './product-card/ProductCard';
import { Filters } from './filters/Filters';

export const ProductList = () => {
    const { categoryName, products, loadMore, loadMoreDisabled} = useProductContext();

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
                <Filters />
                <section>
                    <ul>
                        {products.map((product) => (
                            <ProductCard key={product.id} {...product} />
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
