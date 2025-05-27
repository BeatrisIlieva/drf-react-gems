import { Accordion } from './accordion/Accordion';
import styles from './Filters.module.css';

import { useProductListContext } from '../../../../contexts/ProductListContext';

export const Filters = () => {
    const { filtersData: data } = useProductListContext();
    return (
        <aside className={styles['filters']}>
            {Object.values(data).map((value) => (
                <Accordion key={value.title} data={value} />
            ))}
        </aside>
    );
};
