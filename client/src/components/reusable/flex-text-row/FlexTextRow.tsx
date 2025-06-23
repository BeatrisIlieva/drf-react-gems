import React from 'react';
import styles from './FlexTextRow.module.scss';

interface FlexTextRowProps {
    firstWord: string;
    secondWord: string;
    firstWordImportance?: string;
    secondWordImportance?: string;
    rowImportance?: string;
}

export const FlexTextRow: React.FC<FlexTextRowProps> = ({
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
