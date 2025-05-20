// import { useState, useEffect, useCallback } from 'react';
// import { useLocation } from 'react-router';
// import { useProducts } from '../../../api/productsApi';

// import styles from './ProductList.module.css';
// import { ProductCard } from './product-card/ProductCard';
// import { Filters } from './filters/Filters';

// const initialFiltersData = {
//     materials: { title: 'Material', elements: {} },
//     prices: { title: 'Price', elements: {} },
//     colors: { title: 'Color', elements: {} },
//     stones: { title: 'Stone', elements: {} },
//     categories: { title: 'Category', elements: {} },
//     sizes: { title: 'Size', elements: {} },
//     collections: { title: 'Collection', elements: {} }
// };

// export const ProductList = () => {
//     const [categoryName, setCategoryName] = useState([]);
//     const [categoryId, setCategoryId] = useState(null);
//     const [products, setProducts] = useState([]);
//     const [totalProductsCount, setTotalProductsCount] = useState(0);
//     const [page, setPage] = useState(1);
//     const location = useLocation();
//     const { getProducts } = useProducts();
//     const [loadMoreDisabled, setLoadMoreDisabled] = useState(false);
//     const [filtersData, setFiltersData] = useState(initialFiltersData);
//     const [colorIds, setColorIds] = useState([]);
//     const [stoneIds, setStoneIds] = useState([]);
//     const [stonesData, setStonesData] = useState({});
//     const [colorsData, setColorsData] = useState({});
//     const [materialsData, setMaterialsData] = useState({});
//     const [materialIds, setMaterialIds] = useState([]);

//     useEffect(() => {
//         setColorsData({});
//         setColorIds([]);
//         setStonesData({});
//         setStoneIds([]);
//         setMaterialsData({});
//         setMaterialIds([]);
//         setPage(1);
//     }, [location]);

//     const updateColors = useCallback(
//         (updatedColors) => {
//             setColorIds(updatedColors);

//             const nextPage = 1;
//             setPage(nextPage);

//             getProducts({
//                 categoryId,
//                 pageNumber: nextPage,
//                 colorIds: updatedColors,
//                 stoneIds: stoneIds
//             })
//                 .then((response) => {
//                     setProducts(response.results);
//                     setTotalProductsCount(response.count);

//                     setStonesData(response.stones_by_count);
//                     setColorsData(response.colors_by_count);
//                 })
//                 .catch((err) => console.log(err.message));
//         },
//         [getProducts, categoryId, stoneIds]
//     );

//     const addColorToFiltration = useCallback(
//         (colorId) => {
//             const updatedColors = [...colorIds, colorId];

//             updateColors(updatedColors);
//         },
//         [colorIds, updateColors]
//     );

//     const removeColorFromFiltration = useCallback(
//         (colorId) => {
//             const updatedColors = [...colorIds];
//             const result = updatedColors.filter((id) => id !== colorId);

//             updateColors(result);
//         },
//         [colorIds, updateColors]
//     );

//     const updateStones = useCallback(
//         (updatedStones) => {
//             setStoneIds(updatedStones);

//             const nextPage = 1;
//             setPage(nextPage);

//             getProducts({
//                 categoryId,
//                 pageNumber: nextPage,
//                 stoneIds: updatedStones,
//                 colorIds: colorIds
//             })
//                 .then((response) => {
//                     setProducts(response.results);
//                     setTotalProductsCount(response.count);

//                     setStonesData(response.stones_by_count);
//                     setColorsData(response.colors_by_count);
//                 })
//                 .catch((err) => console.log(err.message));
//         },
//         [getProducts, categoryId, colorIds]
//     );

//     const addStoneToFiltration = useCallback(
//         (stoneId) => {
//             const updatedStones = [...stoneIds, stoneId];

//             updateStones(updatedStones);
//         },
//         [stoneIds, updateStones]
//     );

//     const removeStoneFromFiltration = useCallback(
//         (stoneId) => {
//             const updatedStones = [...stoneIds];
//             const result = updatedStones.filter((id) => id !== stoneId);

//             updateStones(result);
//         },
//         [stoneIds, updateStones]
//     );

//     useEffect(() => {
//         setLoadMoreDisabled(() => totalProductsCount <= products.length);
//     }, [products, totalProductsCount, location]);

//     useEffect(() => {
// const pathItems = location.pathname.split('/').splice(1);
// const itemName = pathItems[1];
// const itemId = pathItems[2];

// const nameCapitalized = itemName.charAt(0).toUpperCase() + itemName.slice(1) + 's';

//         setCategoryName(nameCapitalized);
//         setCategoryId(itemId);

//         getProducts({ categoryId: itemId })
//             .then((response) => {
//                 setProducts(response.results);
//                 setStonesData(response.stones_by_count);
//                 setColorsData(response.colors_by_count);
//                 setTotalProductsCount(response.count);
//                 setColorsData(response.materials_by_count);

//                 setFiltersData((state) => ({
//                     ...state,
//                     colors: {
//                         ...state.colors,
//                         elements: response.colors_by_count
//                     }
//                 }));
//             })
//             .catch((err) => console.log(err.message));
//     }, [location, getProducts]);

//     const loadMoreHandler = () => {
//         if (totalProductsCount <= products.length) return;
//         const nextPage = page + 1;
//         setPage(nextPage);

//         getProducts({ categoryId, pageNumber: nextPage, colorIds })
//             .then((response) => {
//                 setProducts((prev) => {
//                     const updatedProducts = [...prev, ...response.results];

//                     return updatedProducts;
//                 });
//             })
//             .catch((err) => console.log(err.message));
//     };

//     return (
//         <section className={styles['product-list']}>
//             <header>
//                 <h2>{categoryName}</h2>
//             </header>
//             <nav className={styles['secondary']}>
//                 <ul>
//                     <li>Filters</li>
//                     <li>Sort By</li>
//                 </ul>
//             </nav>
//             <div>
//                 <Filters
//                     stonesData={stonesData}
//                     colorsData={colorsData}
//                     data={filtersData}
//                     addColorToFiltration={addColorToFiltration}
//                     removeColorFromFiltration={removeColorFromFiltration}
//                     addStoneToFiltration={addStoneToFiltration}
//                     removeStoneFromFiltration={removeStoneFromFiltration}
//                 />
//                 <section>
//                     <ul>
//                         {products.length > 0 &&
//                             products.map((product) => (
//                                 <ProductCard key={product.id} {...product} />
//                             ))}
//                     </ul>
//                     <button onClick={loadMoreHandler} disabled={loadMoreDisabled}>
//                         Load More
//                     </button>
//                 </section>
//             </div>
//         </section>
//     );
// };

import { useProductContext } from '../../../contexts/ProductContext';
import styles from './ProductList.module.css';
import { ProductCard } from './product-card/ProductCard';
import { Filters } from './filters/Filters';

export const ProductList = () => {
    const { categoryName, products, loadMore, loadMoreDisabled } = useProductContext();

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
