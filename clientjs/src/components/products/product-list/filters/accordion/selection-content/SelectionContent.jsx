import styles from './SelectionContent.module.css';

export const SelectionContent = ({ clickHandler, itemId, title, count }) => {
    return (
        <span onClick={() => clickHandler(itemId)} className={styles['selection-content']}>
            <span>{title}</span>
            <span>({count})</span>
        </span>
    );
};
