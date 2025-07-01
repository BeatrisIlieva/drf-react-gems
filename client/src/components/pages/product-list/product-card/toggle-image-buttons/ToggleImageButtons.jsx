import styles from './ToggleImageButtons.module.scss';
import { Button } from './button/Button';

export const ToggleImageButtons = ({
    selectedIndex,
    onSelect,
    buttonsCount = 2
}) => {
    return (
        <div className={styles['toggle-image-buttons']}>
            {Array.from({ length: buttonsCount }).map(
                (_, index) => (
                    <Button
                        key={index}
                        onClick={() => onSelect(index)}
                        isSelected={selectedIndex === index}
                    />
                )
            )}
        </div>
    );
};
