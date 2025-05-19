import { Accordion } from './accordion/Accordion';
import styles from './Filters.module.css';

export const Filters = ({ data }) => {
    return (
        <aside className={styles['filters']}>
            {Object.values(data).map((value, index, array) => (
                <Accordion
                    key={value.title}
                    data={value}
                    isLast={index === array.length - 1}
                />
            ))}
        </aside>
    );
};
