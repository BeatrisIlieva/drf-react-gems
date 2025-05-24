import { Accordion } from './accordion/Accordion';
import styles from './Filters.module.css';

import { useProductContext } from '../../../../contexts/ProductContext';

export const Filters = () => {
    const { filtersData: data } = useProductContext();
    return (
        <aside className={styles['filters']}>
            {Object.values(data).map((value) => (
                <Accordion key={value.title} data={value} />
            ))}
        </aside>
    );
};
