import type { ReactElement } from 'react';

import styles from './ToggleImageButtons.module.scss';
import { Button } from './button/Button';

interface Props {
    selectedIndex: number;
    onSelect: (index: number) => void;
    buttonsCount?: number;
}

export const ToggleImageButtons = ({
    selectedIndex,
    onSelect,
    buttonsCount = 2
}: Props): ReactElement => {
    return (
        <div className={styles['toggle-image-buttons']}>
            {Array.from({ length: buttonsCount }).map((_, index) => (
                <Button
                    key={index}
                    onClick={() => onSelect(index)}
                    isSelected={selectedIndex === index}
                />
            ))}
        </div>
    );
};
