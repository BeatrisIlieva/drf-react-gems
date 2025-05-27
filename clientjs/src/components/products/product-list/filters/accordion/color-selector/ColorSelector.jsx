import { useProductListContext } from '../../../../../../contexts/ProductListContext';
import { ColorItem } from './color-item/ColorItem';

export const ColorSelector = () => {
    const { colorsData } = useProductListContext();

    return (
        <>
            {Object.entries(colorsData).map(([color, value]) => (
                <ColorItem key={color} {...value} />
            ))}
        </>
    );
};
