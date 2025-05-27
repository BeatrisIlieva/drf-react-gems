import { useProductListContext } from '../../../../../../contexts/ProductListContext';
import { MaterialItem } from './material-item/MaterialItem';

export const MaterialSelector = () => {
    const { materialsData } = useProductListContext();

    return (
        <>
            {materialsData.length > 0 &&
                materialsData.map((item) => <MaterialItem key={item.material__id} {...item} />)}
        </>
    );
};
