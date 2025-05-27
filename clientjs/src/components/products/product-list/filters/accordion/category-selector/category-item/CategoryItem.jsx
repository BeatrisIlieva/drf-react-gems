import { useProductListContext } from '../../../../../../../contexts/ProductListContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

export const CategoryItem = ({
    reference__name: title,
    reference__id: itemId,
    category_count: count
}) => {
    const { addCategoryToFiltration, removeCategoryFromFiltration } = useProductListContext();

    return (
        <SelectionContent
            addHandler={addCategoryToFiltration}
            removeHandler={removeCategoryFromFiltration}
            itemId={itemId}
            title={title}
            count={count}
        />
    );
};
