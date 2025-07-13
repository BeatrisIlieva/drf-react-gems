import { ProductDataProvider } from './ProductDataProvider';

export const ProductItemProvider = ({ children }) => {
    return <ProductDataProvider>{children}</ProductDataProvider>;
};
