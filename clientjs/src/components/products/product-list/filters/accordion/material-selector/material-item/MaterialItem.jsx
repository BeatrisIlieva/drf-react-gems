import { useProductListContext } from '../../../../../../../contexts/ProductListContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

export const MaterialItem = ({
    material__name: title,
    material__id: itemId,
    material_count: count
}) => {
    const { addMaterialToFiltration, removeMaterialFromFiltration } = useProductListContext();

    return (
        <SelectionContent
            addHandler={addMaterialToFiltration}
            removeHandler={removeMaterialFromFiltration}
            itemId={itemId}
            title={title}
            count={count}
        />
    );
};
