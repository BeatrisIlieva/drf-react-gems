import styles from './DeleteButton.module.scss';

export const DeleteButton = ({ entityName, callbackHandler }) => {
    return (
        <button className={styles['delete-button']} onClick={callbackHandler}>
            Delete {entityName}
        </button>
    );
};
