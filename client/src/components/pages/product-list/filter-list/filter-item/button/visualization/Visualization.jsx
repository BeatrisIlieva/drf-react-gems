import styles from './Visualization.module.scss';

export const Visualization = ({ item }) => {
    if (item.hex) {
        const className = [styles['visualization'], item.label === 'White' ? styles['white'] : '']
            .filter(Boolean)
            .join(' ');

        return <span className={className} style={{ backgroundColor: item.hex }} />;
    }

    if (item.image) {
        return (
            <span className={styles['visualization']}>
                <img src={item.image} alt={item.label} />
            </span>
        );
    }

    return null;
};
