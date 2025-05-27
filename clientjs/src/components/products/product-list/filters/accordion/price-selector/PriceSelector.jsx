import { useProductListContext } from '../../../../../../contexts/ProductListContext';
import { PriceItem } from './price-item/PriceItem';

export const PriceSelector = () => {
    const { pricesData } = useProductListContext();

    return (
        <>
            {pricesData.length > 0 &&
                pricesData.map((item) => <PriceItem key={item.price_range} {...item} />)}
        </>
    );
};
