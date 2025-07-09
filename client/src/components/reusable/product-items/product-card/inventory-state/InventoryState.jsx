import styles from './InventoryState.module.scss';

export const InventoryState = ({ positive, label }) => {
    return (
        <div className={styles['inventory-state']}>
            <span className={positive === false ? `${styles['on']}` : `${styles['off']}`}></span>
            <span>{label}</span>
        </div>
    );
};
