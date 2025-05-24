import { useProductContext } from '../../../../../../contexts/ProductContext';
import { PriceItem } from './price-item/PriceItem';

export const PriceSelector = () => {
    const { pricesData } = useProductContext();
    console.log(pricesData)

    return (
        <>
            {pricesData.length > 0 &&
                pricesData.map((item) => <PriceItem key={item.price_range} {...item} />)}
        </>
    );
};
