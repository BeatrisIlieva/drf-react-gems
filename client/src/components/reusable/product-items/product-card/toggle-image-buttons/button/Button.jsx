import styles from './Button.module.scss';

export const Button = ({ onClick, isSelected }) => {
    return <button onClick={onClick} className={styles['button']} disabled={isSelected}></button>;
};
