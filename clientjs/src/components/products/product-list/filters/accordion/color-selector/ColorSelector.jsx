import styles from './ColorSelector.module.css';

export const ColorSelector = ({ color, count, hex, colorId, updateColors}) => {
    return (
        <span className={styles['color-selector']} onClick={() => updateColors(colorId)}>
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
