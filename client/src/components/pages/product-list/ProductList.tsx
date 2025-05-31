import { useEffect, type ReactElement } from 'react';
import { useProductListContext } from '../../../contexts/ProductListContext';
import { useParams } from 'react-router';

export const ProductList = (): ReactElement => {
    const { data, loading, error, fetchProducts } = useProductListContext();
    const { categoryName } = useParams();

    useEffect(() => {
        if(categoryName) {
            fetchProducts({ categoryName, pageNumber: '1' });
        }
    }, [fetchProducts, categoryName]);

    if (loading) return <p>Loading products...</p>;
    if (error) return <p>Error: {error}</p>;

    console.log(data)

    return (
        <div>
            <h2>Products</h2>
            {data?.results.map((product) => (
                <div key={product.id}>
                    <p>{product.collectionName}</p>
                    <img src={product.firstImage} alt="" />
                </div>
            ))}
        </div>
    );
};
