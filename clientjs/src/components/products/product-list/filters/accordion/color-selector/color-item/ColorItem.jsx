import { useProductListContext } from '../../../../../../../contexts/ProductListContext';
import { SelectionContent } from '../../selection-content/SelectionContent';

import styles from './ColorItem.module.css';

export const ColorItem = ({ title, count, hex_code, id }) => {
    const { addColorToFiltration, removeColorFromFiltration } = useProductListContext();

    return (
        <SelectionContent
            addHandler={addColorToFiltration}
            removeHandler={removeColorFromFiltration}
            itemId={id}
            title={title}
            count={count}
        >
            <span
                style={{ backgroundColor: hex_code }}
                className={`${hex_code === '#fff' ? styles['white'] : ''}`.trim()}
            ></span>
        </SelectionContent>
    );
};
