import { type ReactElement } from 'react';

import { useToggleDisplayModal } from '../../../../../hooks/useToggleDisplayModal';
import styles from './SortBy.module.scss';
import { ChevronToggle } from '../../../../reusable/chevron-toggle/ChevronToggle';
import { useProductListContext } from '../../../../../contexts/ProductListContext';

const SORT_OPTIONS = [
    { value: 'rating', label: 'Best Rating' },
    { value: 'in_stock', label: 'Available Now' },
    { value: 'price_asc', label: 'Price: Low to High' },
    { value: 'price_desc', label: 'Price: High to Low' }
];

export const SortBy = (): ReactElement => {
    const { displayModal, containerRef, toggleDisplayModal } = useToggleDisplayModal();
    const { updateOrderingCriteria, orderingCriteria } = useProductListContext();

    return (
        <li className={styles['sort-by']} ref={containerRef}>
            <span
                onClick={toggleDisplayModal}
                role='button'
                aria-haspopup='true'
                aria-expanded={displayModal}
                aria-controls='sort-options'
            >
                sort by
            </span>
            <ChevronToggle onToggle={toggleDisplayModal} isOpen={displayModal} />

            {displayModal && (
                <span className={styles['menu']} id='sort-options' role='menu'>
                    {SORT_OPTIONS.map(({ value, label }) => (
                        <button
                            key={value}
                            className={`${orderingCriteria === value && styles['selected']}`}
                            onClick={() => updateOrderingCriteria(value)}
                        >
                            {label}
                        </button>
                    ))}
                </span>
            )}
        </li>
    );
};
