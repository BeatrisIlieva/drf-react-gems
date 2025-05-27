import { useProductListContext } from '../../../../../../../contexts/ProductListContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

export const StoneItem = ({ title, count, image, id }) => {
    const { addStoneToFiltration, removeStoneFromFiltration } = useProductListContext();

    return (
        <SelectionContent
            addHandler={addStoneToFiltration}
            removeHandler={removeStoneFromFiltration}
            itemId={id}
            title={title}
            count={count}
        >
            <span>
                <img src={image} alt={`${title}`} />
            </span>
        </SelectionContent>
    );
};
