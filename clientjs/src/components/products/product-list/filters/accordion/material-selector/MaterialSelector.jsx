import { useProductContext } from '../../../../../../contexts/ProductContext';
import { MaterialItem } from './material-item/MaterialItem';

export const MaterialSelector = () => {
    const { materialsData } = useProductContext();

    return (
        <>
            {materialsData.length > 0 &&
                materialsData.map((item) => <MaterialItem key={item.material__id} {...item} />)}
        </>
    );
};
