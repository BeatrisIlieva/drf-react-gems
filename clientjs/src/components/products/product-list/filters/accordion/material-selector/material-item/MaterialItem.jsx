import { SelectionBox } from '../../selection-box/SelectionBox';
import { useProductContext } from '../../../../../../../contexts/ProductContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

export const MaterialItem = ({
    material__name: title,
    material__id: itemId,
    material_count: count
}) => {
    const { addMaterialToFiltration, removeMaterialFromFiltration } = useProductContext();

    return (
        <SelectionBox removeHandler={removeMaterialFromFiltration} itemId={itemId}>
            <SelectionContent
                clickHandler={addMaterialToFiltration}
                itemId={itemId}
                title={title}
                count={count}
            />
        </SelectionBox>
    );
};
