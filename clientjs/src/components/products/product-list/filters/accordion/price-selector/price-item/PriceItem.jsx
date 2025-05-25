import { useProductContext } from '../../../../../../../contexts/ProductContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

export const PriceItem = ({ price_range: title, count: count }) => {
    const { addPriceToFiltration, removePriceFromFiltration } = useProductContext();

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
