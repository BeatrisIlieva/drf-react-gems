import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { useLocation } from 'react-router';
import { useProducts } from '../api/productsApi';

const ProductContext = createContext();

export const useProductContext = () => useContext(ProductContext);

export const ProductProvider = ({ children }) => {
    const [categoryName, setCategoryName] = useState('');
    const [categoryId, setCategoryId] = useState(null);
    const [products, setProducts] = useState([]);
    const [totalProductsCount, setTotalProductsCount] = useState(0);
    const [page, setPage] = useState(1);
    const [filtersData, setFiltersData] = useState({
        materials: { title: 'Material', elements: {} },
        prices: { title: 'Price', elements: {} },
        colors: { title: 'Color', elements: {} },
        stones: { title: 'Stone', elements: {} },
        categories: { title: 'Category', elements: {} },
        sizes: { title: 'Size', elements: {} },
        collections: { title: 'Collection', elements: {} }
    });
    const [colorIds, setColorIds] = useState([]);
    const [stoneIds, setStoneIds] = useState([]);
    const [materialsData, setMaterialsData] = useState({});
    const [stonesData, setStonesData] = useState({});
    const [colorsData, setColorsData] = useState({});
    const [loadMoreDisabled, setLoadMoreDisabled] = useState(false);

    const { getProducts } = useProducts();
    const location = useLocation();

    useEffect(() => {
        setColorIds([]);
        setStoneIds([]);
        setMaterialsData({});
        setStonesData({});
        setColorsData({});
        setPage(1);
    }, [location]);

    useEffect(() => {
        setLoadMoreDisabled(totalProductsCount <= products.length);
    }, [products, totalProductsCount]);

    useEffect(() => {
        const pathItems = location.pathname.split('/').splice(1);
        const itemName = pathItems[1];
        const itemId = pathItems[2];

        const nameCapitalized = itemName.charAt(0).toUpperCase() + itemName.slice(1) + 's';

        setCategoryName(nameCapitalized);
        setCategoryId(itemId);

        getProducts({ categoryId: itemId }).then((response) => {
            setProducts(response.results);
            setStonesData(response.stones_by_count);
            setColorsData(response.colors_by_count);
            setMaterialsData(response.materials_by_count);
            setTotalProductsCount(response.count);

            setFiltersData((prev) => ({
                ...prev,
                colors: { ...prev.colors, elements: response.colors_by_count }
            }));
        });
    }, [location, getProducts]);

    const updateColors = useCallback((updatedColors) => {
        setColorIds(updatedColors);
        const nextPage = 1;
        setPage(nextPage);
        getProducts({ categoryId, pageNumber: nextPage, colorIds: updatedColors, stoneIds }).then((res) => {
            setProducts(res.results);
            setTotalProductsCount(res.count);
            setStonesData(res.stones_by_count);
            setColorsData(res.colors_by_count);
        });
    }, [categoryId, getProducts, stoneIds]);

    const updateStones = useCallback((updatedStones) => {
        setStoneIds(updatedStones);
        const nextPage = 1;
        setPage(nextPage);
        getProducts({ categoryId, pageNumber: nextPage, stoneIds: updatedStones, colorIds }).then((res) => {
            setProducts(res.results);
            setTotalProductsCount(res.count);
            setStonesData(res.stones_by_count);
            setColorsData(res.colors_by_count);
        });
    }, [categoryId, getProducts, colorIds]);

    const loadMore = () => {
        if (totalProductsCount <= products.length) return;
        const nextPage = page + 1;
        setPage(nextPage);
        getProducts({ categoryId, pageNumber: nextPage, colorIds }).then((res) => {
            setProducts((prev) => [...prev, ...res.results]);
        });
    };

    return (
        <ProductContext.Provider value={{
            categoryName,
            products,
            loadMore,
            loadMoreDisabled,
            filtersData,
            colorIds,
            stoneIds,
            addColorToFiltration: (id) => updateColors([...colorIds, id]),
            removeColorFromFiltration: (id) => updateColors(colorIds.filter((c) => c !== id)),
            addStoneToFiltration: (id) => updateStones([...stoneIds, id]),
            removeStoneFromFiltration: (id) => updateStones(stoneIds.filter((s) => s !== id)),
            colorsData,
            stonesData
        }}>
            {children}
        </ProductContext.Provider>
    );
};
