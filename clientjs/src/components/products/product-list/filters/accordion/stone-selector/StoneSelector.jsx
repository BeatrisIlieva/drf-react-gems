import { useProductContext } from '../../../../../../contexts/ProductContext';
import { StoneItem } from './stone-item/StoneItem';

export const StoneSelector = () => {
    const { stonesData } = useProductContext();

    return (
        <>
            {Object.entries(stonesData).map(([stone, value]) => (
                <StoneItem key={stone} {...value} />
            ))}
        </>
    );
};
