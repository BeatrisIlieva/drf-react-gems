import { useProductContext } from '../../../../../../contexts/ProductContext';
import { CollectionItem } from './collection-item/CollectionItem';

export const CollectionSelector = () => {
    const { collectionsData } = useProductContext();

    return (
        <>
            {collectionsData.length > 0 &&
                collectionsData.map((item) => <CollectionItem key={item.collection__id} {...item} />)}
        </>
    );
};
