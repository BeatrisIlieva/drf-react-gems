import {
    createContext,
    useContext,
    useEffect,
    useState,
    useCallback
} from 'react';
import { useProductItem } from '../api/productsApi';
import { useParams } from 'react-router';
import { useShoppingBag } from '../api/useShoppingBagApi';

const ProductListContext = createContext();

export const useProductItemContext = () => useContext(ProductListContext);

export const ProductItemProvider = ({ children }) => {
    const [product, setProduct] = useState(null);
    const { categoryName, productId } = useParams();
    const { getProduct } = useProductItem();
    const { addToBag } = useShoppingBag();

    const [selectedSize, setSelectedSize] = useState(null);
    const [selectedInventory, setSelectedInventory] = useState({});
    const [
        displayNotSelectedSizeErrorMessage,
        setDisplayNotSelectedSizeErrorMessage
    ] = useState(false);

    const selectSizeClickHandler = (size) => {
        if (selectedSize === null) {
            setSelectedSize(size);
        } else if (selectedSize === size) {
            setSelectedSize(null);
            setSelectedInventory({});
        } else {
            setSelectedSize(size);
        }
    };

    const updateSelectedInventoryHandler = (contentType, objectId) => {
        setSelectedInventory({
            quantity: 1,
            contentType,
            objectId
        });
    };

    const addToBagHandler = () => {
        if (selectedSize === null) {
            setDisplayNotSelectedSizeErrorMessage(true);
        } else {
            addToBag(selectedInventory);
        }
    };

    useEffect(() => {
        getProduct({ categoryName, productId }).then((result) =>
            setProduct(result)
        );
    }, [categoryName, productId, getProduct]);

    const productCategory =
        categoryName.charAt(0).toUpperCase() + categoryName.slice(1);
    const productDescription = `${product?.stone_by_color.color.name} ${product?.stone_by_color.stone.name}s set in ${product?.material.name}`;

    return (
        <ProductListContext.Provider
            value={{
                product,
                productCategory,
                productDescription,
                categoryName,
                selectedSize,
                selectSizeClickHandler,
                updateSelectedInventoryHandler,
                displayNotSelectedSizeErrorMessage,
                addToBagHandler
            }}
        >
            {children}
        </ProductListContext.Provider>
    );
};
