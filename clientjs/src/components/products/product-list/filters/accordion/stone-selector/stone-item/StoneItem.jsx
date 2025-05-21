import { useProductContext } from '../../../../../../../contexts/ProductContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

export const StoneItem = ({ title, count, image, id }) => {
    const { addStoneToFiltration, removeStoneFromFiltration } = useProductContext();

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
