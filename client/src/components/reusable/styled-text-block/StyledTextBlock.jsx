import styles from './StyledTextBlock.module.scss';

export const StyledTextBlock = ({ text, fontSize, isSubtle, isLighter }) => {
    const words = text.trim().split(' ');

    return (
        <p
            className={styles['styled-text-block']}
            style={{
                fontSize: fontSize ? `${fontSize}em` : `${1}em`,
                opacity: isSubtle ? 0.6 : 1,
                fontWeight: isLighter ? 300 : 400,
            }}
        >
            {words.map((word, index) => (
                <span key={index}>{word}</span>
            ))}
        </p>
    );
};
