import { useProductListContext } from '../../../../../../../contexts/ProductListContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

export const PriceItem = ({ price_range: title, count: count }) => {
    const { addPriceToFiltration, removePriceFromFiltration } = useProductListContext();

    return (
        <SelectionContent
            addHandler={addPriceToFiltration}
            removeHandler={removePriceFromFiltration}
            itemId={title}
            title={title}
            count={count}
        />
    );
};
