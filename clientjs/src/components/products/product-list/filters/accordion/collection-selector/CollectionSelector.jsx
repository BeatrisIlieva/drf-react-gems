import { useProductListContext } from '../../../../../../contexts/ProductListContext';
import { CollectionItem } from './collection-item/CollectionItem';

export const CollectionSelector = () => {
    const { collectionsData } = useProductListContext();

    return (
        <>
            {collectionsData.length > 0 &&
                collectionsData.map((item) => (
                    <CollectionItem key={item.collection__id} {...item} />
                ))}
        </>
    );
};
