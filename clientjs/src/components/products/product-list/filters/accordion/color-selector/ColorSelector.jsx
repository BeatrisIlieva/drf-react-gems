import styles from './ColorSelector.module.css';

export const ColorSelector = ({ color, count, hex }) => {
    console.log(hex);
    return (
        <span className={styles['color-selector']}>
            <span
                style={{ backgroundColor: hex }}
                className={`${hex === '#fff' ? styles['white'] : ''}`.trim()}
            ></span>
            <span>
                <span>{color}</span>
                <span>({count})</span>
            </span>
        </span>
    );
};
