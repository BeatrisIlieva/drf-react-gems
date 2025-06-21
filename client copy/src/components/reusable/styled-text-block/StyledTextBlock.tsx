import type { ReactElement } from 'react';

import styles from './StyledTextBlock.module.scss';

interface Props {
    text: string;
    fontSize?: number;
    isSubtle?: boolean;
    isLighter?: boolean;
}

export const StyledTextBlock = ({
    text,
    fontSize,
    isSubtle,
    isLighter
}: Props): ReactElement => {
    const words = text.trim().split(' ');

    return (
        <p
            className={styles['styled-text-block']}
            style={{
                fontSize: fontSize ? `${fontSize}em` : `${1}em`,
                opacity: isSubtle ? 0.6 : 1,
                fontWeight: isLighter ? 300 : 400
            }}
        >
            {words.map((word, index) => (
                <span key={index}>{word}</span>
            ))}
        </p>
    );
};
