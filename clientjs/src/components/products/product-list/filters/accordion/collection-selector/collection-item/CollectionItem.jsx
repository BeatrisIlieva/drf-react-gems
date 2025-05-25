import { useProductContext } from '../../../../../../../contexts/ProductContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

export const CollectionItem = ({
    collection__name: title,
    collection__id: itemId,
    collection_count: count
}) => {
    const { addCollectionToFiltration, removeCollectionFromFiltration } = useProductContext();

    return (
        <SelectionContent
            addHandler={addCollectionToFiltration}
            removeHandler={removeCollectionFromFiltration}
            itemId={itemId}
            title={title}
            count={count}
        />
    );
};
