import { Button } from '../button/Button';

import styles from './Deletion.module.scss';

export const Deletion = ({ entityName, onProceed, onCancel }) => {
    return (
        <section className={styles['deletion']}>
            <h3>Delete {entityName}</h3>

            <p>Are you sure you want to delete your {entityName}?</p>

            <div className={styles['buttons-wrapper']}>
                <Button
                    title="Yes, Delete"
                    buttonGrow="1"
                    color="black"
                    callbackHandler={onProceed}
                />
                <Button title="Cancel" buttonGrow="1" color="white" callbackHandler={onCancel} />
            </div>
        </section>
    );
};
