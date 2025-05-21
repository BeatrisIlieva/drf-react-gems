import { useProductContext } from '../../../../../../contexts/ProductContext';
import { ColorItem } from './color-item/ColorItem';

export const ColorSelector = () => {
    const { colorsData } = useProductContext();

    return (
        <>
            {Object.entries(colorsData).map(([color, value]) => (
                <ColorItem key={color} {...value} />
            ))}
        </>
    );
};
