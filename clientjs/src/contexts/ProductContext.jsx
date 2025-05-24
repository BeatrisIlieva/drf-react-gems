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
        sizes: { title: 'Size', elements: {} },
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

    const [loadMoreDisabled, setLoadMoreDisabled] = useState(false);

    const { getProducts } = useProducts();
    const location = useLocation();

    useEffect(() => {
        setColorIds([]);
        setStoneIds([]);
        setStonesData({});
        setColorsData({});
        setMaterialsData({});
        setMaterialIds([]);
        setPage(1);
    }, [location]);

    useEffect(() => {
        setLoadMoreDisabled(totalProductsCount <= products.length);
    }, [products, totalProductsCount]);

    const updateFiltersData = useCallback((response) => {
        setProducts(response.results);
        setStonesData(response.stones_by_count);
        setColorsData(response.colors_by_count);
        setMaterialsData(response.materials_by_count);
        setTotalProductsCount(response.count);
        setPricesData(response.price_ranges)
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

    const updateColors = useCallback(
        (updatedColors) => {
            setColorIds(updatedColors);

            const nextPage = 1;
            setPage(nextPage);

            getProducts({
                categoryName,
                pageNumber: nextPage,
                colorIds: updatedColors,
                stoneIds,
                materialIds
            }).then((response) => {
                updateFiltersData(response);
            });
        },
        [categoryName, getProducts, stoneIds, materialIds, updateFiltersData]
    );

    const updatePrices = useCallback(
        (updatedPrices) => {
            setPrices(updatedPrices);

            const nextPage = 1;
            setPage(nextPage);

            getProducts({
                categoryName,
                pageNumber: nextPage,
                colorIds,
                stoneIds,
                materialIds,
                prices: updatedPrices
            }).then((response) => {
                updateFiltersData(response);
            });
        },
        [categoryName, getProducts, stoneIds, materialIds, updateFiltersData, colorIds]
    );

    const updateStones = useCallback(
        (updatedStones) => {
            setStoneIds(updatedStones);

            const nextPage = 1;
            setPage(nextPage);

            getProducts({
                categoryName,
                pageNumber: nextPage,
                stoneIds: updatedStones,
                colorIds,
                materialIds
            }).then((response) => {
                updateFiltersData(response);
            });
        },
        [categoryName, getProducts, colorIds, materialIds, updateFiltersData]
    );

    const updateMaterials = useCallback(
        (updatedMaterials) => {
            setMaterialIds(updatedMaterials);

            const nextPage = 1;
            setPage(nextPage);

            getProducts({
                categoryName,
                pageNumber: nextPage,
                stoneIds,
                colorIds,
                materialIds: updatedMaterials
            }).then((response) => {
                updateFiltersData(response);
            });
        },
        [categoryName, getProducts, colorIds, stoneIds, updateFiltersData]
    );

    const loadMore = () => {
        if (totalProductsCount <= products.length) return;

        const nextPage = page + 1;
        setPage(nextPage);

        getProducts({ categoryName, pageNumber: nextPage, colorIds }).then((res) => {
            setProducts((prev) => [...prev, ...res.results]);
        });
    };

    console.log(pricesData)

    return (
        <ProductContext.Provider
            value={{
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
                addMaterialToFiltration: (id) => updateMaterials([...materialIds, id]),
                removeMaterialFromFiltration: (id) =>
                    updateMaterials(materialIds.filter((s) => s !== id)),
                addPricesToFiltration: (price) => updatePrices([...prices, price]),
                removePricesFromFiltration: (price) => updatePrices(prices.filter((s) => s !== price)),
                colorsData,
                stonesData,
                materialsData,
                pricesData
            }}
        >
            {children}
        </ProductContext.Provider>
    );
};
