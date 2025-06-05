import { useEffect, useRef, useState, type ReactElement } from 'react';

import styles from './FilterItem.module.scss';
import type { NormalizedFilterItem } from '../../../../../types/NormalizedFilter';
import { Icon } from '../../../../reusable/icon/Icon';
import { useProductListContext } from '../../../../../contexts/ProductListContext';
import { ChevronToggle } from '../../../../reusable/chevron-toggle/ChevronToggle';
import { useCategoryName } from '../../../../../hooks/useCategoryName';

interface FilterItemProps {
    label: 'Collection' | 'Color' | 'Metal' | 'Stone';
    data: NormalizedFilterItem[];
}

export const FilterItem = ({ label, data }: FilterItemProps): ReactElement => {
    const { updateEntityCharacteristics, entityStateMapper } = useProductListContext();

    const { categoryName } = useCategoryName();

    const [displayFilter, setDisplayFilter] = useState<boolean>(false);

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
    }, [displayFilter, data]);

    useEffect(() => {
        setDisplayFilter(false);
    }, [categoryName]);

    const clickHandler = (itemId: string | number) => {
        updateEntityCharacteristics(label, itemId as number);
    };

    return (
        <li className={styles['filter-item']}>
            <div className={styles['label-wrapper']}>
                <h6 onClick={toggleDisplayFilter}>{label}</h6>

                <ChevronToggle isOpen={displayFilter} onToggle={toggleDisplayFilter} />
            </div>
            <ul
                ref={contentRef}
                className={styles['list']}
                style={{
                    maxHeight: height,
                    opacity: displayFilter ? 1 : 0,
                    overflow: 'hidden',
                    transition: 'max-height 0.3s ease, opacity 0.3s ease',
                    marginTop: displayFilter ? '1em' : '0'
                }}
            >
                {data.map((item) => (
                    <li
                        key={item.id}
                        className={`${entityStateMapper[label].includes(item.id) ? styles['selected'] : ''}`.trim()}
                    >
                        <button
                            disabled={entityStateMapper[label].includes(item.id)}
                            className={styles['add-filter']}
                            onClick={() => clickHandler(item.id)}
                        >
                            {item.hex && (
                                <span
                                    className={`${styles['visualization']} ${item.label === 'White' ? styles['white'] : ''}`.trim()}
                                    style={{
                                        backgroundColor: item.hex
                                    }}
                                ></span>
                            )}
                            {item.image && (
                                <span className={styles['visualization']}>
                                    <img src={item.image} alt={item.label} />
                                </span>
                            )}
                            <span>{item.label}</span>
                            <span className={styles['count']}>({item.count})</span>
                        </button>

                        {entityStateMapper[label].includes(item.id) && (
                            <div
                                className={styles['remove-filter']}
                                onClick={() => clickHandler(item.id)}
                            >
                                <Icon name={'xMark'} isSubtle={true} fontSize={0.7} />
                            </div>
                        )}
                    </li>
                ))}
            </ul>
        </li>
    );
};
