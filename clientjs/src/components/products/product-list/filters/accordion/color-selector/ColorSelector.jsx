import styles from './ColorSelector.module.css';

export const ColorSelector = ({ color, count, hex, colorId, addColorToFiltration }) => {
    return (
        <span className={styles['color-selector']} onClick={() => addColorToFiltration(colorId)}>
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
