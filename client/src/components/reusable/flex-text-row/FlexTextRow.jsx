import styles from './FlexTextRow.module.scss';

export const FlexTextRow = ({
    firstWord,
    secondWord,
    firstWordImportance,
    secondWordImportance,
    rowImportance
}) => {
    return (
        <p
            className={`${styles['flex-text-row']} ${
                rowImportance ? styles[rowImportance] : ''
            }`.trim()}
        >
            <span
                className={`${
                    firstWordImportance
                        ? styles[firstWordImportance]
                        : ''
                }`.trim()}
            >
                {firstWord}
            </span>
            <span
                className={`${
                    secondWordImportance
                        ? styles[secondWordImportance]
                        : ''
                }`.trim()}
            >
                {secondWord}
            </span>
        </p>
    );
};
