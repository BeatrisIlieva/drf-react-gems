import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { useLocation } from 'react-router';
import { useProducts } from '../api/productsApi';

const ProductContext = createContext();

export const useProductContext = () => useContext(ProductContext);

export const ProductProvider = ({ children }) => {
    const [categoryName, setCategoryName] = useState('');
    const [products, setProducts] = useState([]);
    const [totalProductsCount, setTotalProductsCount] = useState(0);
    const [page, setPage] = useState(1);
    const [filtersData, setFiltersData] = useState({
        materials: { title: 'Material', elements: {} },
        prices: { title: 'Price', elements: {} },
        colors: { title: 'Color', elements: {} },
        stones: { title: 'Stone', elements: {} },
        categories: { title: 'Category', elements: {} },
        collections: { title: 'Collection', elements: {} }
    });
    const [colorIds, setColorIds] = useState([]);
    const [stoneIds, setStoneIds] = useState([]);
    const [stonesData, setStonesData] = useState({});
    const [colorsData, setColorsData] = useState({});
    const [materialsData, setMaterialsData] = useState({});
    const [materialIds, setMaterialIds] = useState([]);
    const [pricesData, setPricesData] = useState([]);
    const [prices, setPrices] = useState([]);
    const [collectionsData, setCollectionsData] = useState({});
    const [collectionIds, setCollectionIds] = useState([]);
    const [categoriesData, setCategoriesData] = useState({});
    const [categoryIds, setCategoryIds] = useState([]);

    const [loadMoreDisabled, setLoadMoreDisabled] = useState(false);

    const { getProducts } = useProducts();
    const location = useLocation();

    const resetFilters = () => {
        setColorIds([]);
        setStoneIds([]);
        setStonesData({});
        setColorsData({});
        setMaterialsData({});
        setMaterialIds([]);
        setPricesData([]);
        setPrices([]);
        setCollectionsData({});
        setCollectionIds([]);
        setCategoriesData({});
        setCategoryIds([]);
        setPage(1);
    };

    useEffect(() => {
        resetFilters();
    }, [location]);

    useEffect(() => {
        setLoadMoreDisabled(totalProductsCount <= products.length);
    }, [products, totalProductsCount]);

    const updateFiltersData = useCallback((response) => {
        setProducts(response.results);
        setStonesData(response.stones_by_count);
        setColorsData(response.colors_by_count);
        setCollectionsData(response.collections_by_count);
        setCategoriesData(response.categories_by_count);
        setMaterialsData(response.materials_by_count);
        setTotalProductsCount(response.count);
        setPricesData(response.price_ranges);
    }, []);

    useEffect(() => {
        const pathItems = location.pathname.split('/').splice(1);
        const itemName = pathItems[1];

        const nameCapitalized = itemName.charAt(0).toUpperCase() + itemName.slice(1) + 's';

        setCategoryName(nameCapitalized);
        setCategoryName(itemName);

        getProducts({ categoryName: itemName }).then((response) => {
            updateFiltersData(response);

            setFiltersData((prev) => ({
                ...prev,
                colors: { ...prev.colors, elements: response.colors_by_count }
            }));
        });
    }, [location, getProducts, updateFiltersData]);

    const loadMore = () => {
        if (totalProductsCount <= products.length) return;

        const nextPage = page + 1;
        setPage(nextPage);

        getProducts({
            categoryName,
            pageNumber: nextPage,
            colorIds,
            stoneIds,
            materialIds,
            collectionIds,
            categoryIds
        }).then((res) => {
            setProducts((prev) => [...prev, ...res.results]);
        });
    };

    const updateFilter = useCallback(
        ({ key, value }) => {
            const setters = {
                colorIds: setColorIds,
                stoneIds: setStoneIds,
                materialIds: setMaterialIds,
                prices: setPrices,
                collectionIds: setCollectionIds,
                categoryIds: setCategoryIds
            };

            setters[key](value);
            const nextPage = 1;
            setPage(nextPage);

            getProducts({
                categoryName,
                pageNumber: nextPage,
                colorIds: key === 'colorIds' ? value : colorIds,
                stoneIds: key === 'stoneIds' ? value : stoneIds,
                materialIds: key === 'materialIds' ? value : materialIds,
                collectionIds: key === 'collectionIds' ? value : collectionIds,
                categoryIds: key === 'categoryIds' ? value : categoryIds,
                prices: key === 'prices' ? value : prices
            }).then(updateFiltersData);
        },
        [
            categoryName,
            getProducts,
            colorIds,
            stoneIds,
            materialIds,
            prices,
            updateFiltersData,
            collectionIds,
            categoryIds
        ]
    );

    return (
        <ProductContext.Provider
            value={{
                categoryName,
                products,
                loadMore,
                loadMoreDisabled,
                filtersData,
                addColorToFiltration: (id) =>
                    updateFilter({ key: 'colorIds', value: [...colorIds, id] }),
                removeColorFromFiltration: (id) =>
                    updateFilter({ key: 'colorIds', value: colorIds.filter((c) => c !== id) }),
                addStoneToFiltration: (id) =>
                    updateFilter({ key: 'stoneIds', value: [...stoneIds, id] }),
                removeStoneFromFiltration: (id) =>
                    updateFilter({ key: 'stoneIds', value: stoneIds.filter((s) => s !== id) }),
                addMaterialToFiltration: (id) =>
                    updateFilter({ key: 'materialIds', value: [...materialIds, id] }),
                removeMaterialFromFiltration: (id) =>
                    updateFilter({
                        key: 'materialIds',
                        value: materialIds.filter((m) => m !== id)
                    }),
                addCollectionToFiltration: (id) =>
                    updateFilter({ key: 'collectionIds', value: [...collectionIds, id] }),
                removeCollectionFromFiltration: (id) =>
                    updateFilter({
                        key: 'collectionIds',
                        value: collectionIds.filter((c) => c !== id)
                    }),
                addCategoryToFiltration: (id) =>
                    updateFilter({ key: 'categoryIds', value: [...categoryIds, id] }),
                removeCategoryFromFiltration: (id) =>
                    updateFilter({
                        key: 'categoryIds',
                        value: categoryIds.filter((c) => c !== id)
                    }),
                addPriceToFiltration: (price) =>
                    updateFilter({ key: 'prices', value: [...prices, price] }),
                removePriceFromFiltration: (price) =>
                    updateFilter({ key: 'prices', value: prices.filter((p) => p !== price) }),
                colorsData,
                stonesData,
                materialsData,
                pricesData,
                collectionsData,
                categoriesData
            }}
        >
            {children}
        </ProductContext.Provider>
    );
};
