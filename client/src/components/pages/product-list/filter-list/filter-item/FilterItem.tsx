import {
    useEffect,
    useRef,
    useState,
    type ReactElement
} from 'react';

import styles from './FilterItem.module.scss';
import type { NormalizedFilterItem } from '../../../../../types/NormalizedFilter';
import { Icon } from '../../../../reusable/icon/Icon';

interface FilterItemProps {
    label: string;
    data: NormalizedFilterItem[];
}

export const FilterItem = ({
    label,
    data
}: FilterItemProps): ReactElement => {
    const [displayFilter, setDisplayFilter] =
        useState<boolean>(false);

    const toggleDisplayFilter = (): void => {
        setDisplayFilter(() => !displayFilter);
    };

    const [height, setHeight] = useState<string | number>(0);
    const contentRef = useRef<HTMLUListElement | null>(null);

    useEffect(() => {
        if (displayFilter && contentRef.current) {
            const scrollHeight = contentRef.current.scrollHeight;
            setHeight(scrollHeight);
        } else {
            setHeight(0);
        }
    }, [displayFilter]);

    return (
        <li
            className={styles['filter-item']}
            onClick={toggleDisplayFilter}
        >
            <div className={styles['label-wrapper']}>
                <h5>{label}</h5>

                <span
                    className={`${styles['toggle-icon']} ${displayFilter ? styles['rotated'] : ''}`}
                >
                    <Icon
                        name={displayFilter ? 'arrowUp' : 'arrowDown'}
                        isSubtle={true}
                        fontSize={0.7}
                    />
                </span>
            </div>
            <ul
                ref={contentRef}
                className={styles['list']}
                style={{
                    maxHeight: height,
                    opacity: displayFilter ? 1 : 0,
                    overflow: 'hidden',
                    transition:
                        'max-height 0.3s ease, opacity 0.3s ease',
                    marginTop: displayFilter ? '1em' : '0'
                }}
            >
                {data.map((item) => (
                    <li key={item.id}>
                        <div className={styles['add-filter']}>
                            {item.hex && (
                                <span
                                    className={`${styles['visualization']} ${item.label === 'White' ? styles['white'] : ''}`.trim()}
                                    style={{
                                        backgroundColor: item.hex
                                    }}
                                ></span>
                            )}
                            {item.image && (
                                <span
                                    className={
                                        styles['visualization']
                                    }
                                >
                                    <img
                                        src={item.image}
                                        alt={item.label}
                                    />
                                </span>
                            )}
                            <span>{item.label}</span>
                            <span className={styles['count']}>
                                ({item.count})
                            </span>
                        </div>
                        <div className={styles['remove-filter']}>
                            <Icon
                                name={'xMark'}
                                isSubtle={true}
                                fontSize={0.7}
                            />
                        </div>
                    </li>
                ))}
            </ul>
        </li>
    );
};
