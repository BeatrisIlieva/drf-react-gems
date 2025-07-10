import styles from './Agreement.module.scss';

export const Agreement = ({ agree, agreeError, onToggle }) => {
    return (
        <>
            <div className={styles['terms-wrapper']}>
                <input
                    type="checkbox"
                    name="agree"
                    id="agree"
                    checked={agree}
                    onChange={onToggle}
                />
                <label className={styles['agree']} htmlFor="agree">
                    By creating an account, you agree to receive email updates*
                </label>
            </div>
            {agreeError && <div className={styles['error-message']}>{agreeError}</div>}
        </>
    );
};
