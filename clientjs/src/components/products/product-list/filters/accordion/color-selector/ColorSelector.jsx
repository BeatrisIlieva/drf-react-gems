import styles from './ColorSelector.module.css';

export const ColorSelector = ({ title, count, hex, image, itemId, addFiltration }) => {
    return (
        <span className={styles['color-selector']} onClick={() => addFiltration(itemId)}>
            {hex ? (
                <span
                    style={{ backgroundColor: hex }}
                    className={`${hex === '#fff' ? styles['white'] : ''}`.trim()}
                ></span>
            ) : (
                <span>
                    <img src={image} alt={`${title}`} />
                </span>
            )}
            <span>
                <span>{title}</span>
                <span>({count})</span>
            </span>
        </span>
    );
};
