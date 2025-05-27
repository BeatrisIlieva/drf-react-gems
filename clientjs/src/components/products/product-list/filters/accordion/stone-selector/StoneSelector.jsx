import { useProductListContext } from '../../../../../../contexts/ProductListContext';
import { StoneItem } from './stone-item/StoneItem';

export const StoneSelector = () => {
    const { stonesData } = useProductListContext();

    return (
        <>
            {Object.entries(stonesData).map(([stone, value]) => (
                <StoneItem key={stone} {...value} />
            ))}
        </>
    );
};
