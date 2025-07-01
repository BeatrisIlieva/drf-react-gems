import { useProductListContext } from '../../../../../contexts/ProductListContext';
import { useToggleDisplayModal } from '../../../../../hooks/useToggleDisplayModal';

import { ChevronToggle } from '../../../../reusable/chevron-toggle/ChevronToggle';

import { SORT_OPTIONS } from '../../../../../constants/sortOptions';

import styles from './SortBy.module.scss';

export const SortBy = () => {
    const { displayModal, containerRef, toggleDisplayModal } =
        useToggleDisplayModal();
    const { updateOrdering, ordering } = useProductListContext();

    const clickHandler = (value) => {
        updateOrdering(value);
        toggleDisplayModal();
    };

    const selectedLabel = SORT_OPTIONS.find(
        (option) => option.value === ordering
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
                {ordering ? selectedLabel : 'sort by'}
            </span>
            <ChevronToggle
                onToggle={toggleDisplayModal}
                isOpen={displayModal}
            />

            {displayModal && (
                <span
                    className={styles['menu']}
                    id='sort-options'
                    role='menu'
                >
                    {SORT_OPTIONS.map(({ value, label }) => (
                        <button
                            key={value}
                            className={`${
                                ordering === value &&
                                styles['selected']
                            }`}
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
