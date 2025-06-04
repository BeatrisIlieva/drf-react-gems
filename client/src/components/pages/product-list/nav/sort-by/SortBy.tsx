import { type ReactElement } from 'react';

import { useProductListContext } from '../../../../../contexts/ProductListContext';
import { useToggleDisplayModal } from '../../../../../hooks/useToggleDisplayModal';

import { ChevronToggle } from '../../../../reusable/chevron-toggle/ChevronToggle';

import { SORT_OPTIONS } from '../../../../../constants/sortOptions';

import styles from './SortBy.module.scss';

export const SortBy = (): ReactElement => {
    const { displayModal, containerRef, toggleDisplayModal } = useToggleDisplayModal();
    const { updateOrderingCriteria, orderingCriteria } = useProductListContext();

    const clickHandler = (value: string) => {
        updateOrderingCriteria(value);
        toggleDisplayModal();
    };

    const selectedLabel = SORT_OPTIONS.find(
        (option) => option.value === orderingCriteria
    )?.label;

    return (
        <li className={styles['sort-by']} ref={containerRef}>
            <span
                onClick={toggleDisplayModal}
                role='button'
                aria-haspopup='true'
                aria-expanded={displayModal}
                aria-controls='sort-options'
            >
                {orderingCriteria ? selectedLabel : 'sort by'}
            </span>
            <ChevronToggle onToggle={toggleDisplayModal} isOpen={displayModal} />

            {displayModal && (
                <span className={styles['menu']} id='sort-options' role='menu'>
                    {SORT_OPTIONS.map(({ value, label }) => (
                        <button
                            key={value}
                            className={`${orderingCriteria === value && styles['selected']}`}
                            onClick={() => clickHandler(value)}
                        >
                            {label}
                        </button>
                    ))}
                </span>
            )}
        </li>
    );
};
