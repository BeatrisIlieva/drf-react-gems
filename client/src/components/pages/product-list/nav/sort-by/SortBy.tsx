import { type ReactElement } from 'react';

import { useToggleDisplayModal } from '../../../../../hooks/useToggleDisplayModal';

import styles from './SortBy.module.scss';
import { ChevronToggle } from '../../../../reusable/chevron-toggle/ChevronToggle';

export const SortBy = (): ReactElement => {
    const { displayModal, containerRef, toggleDisplayModal } =
        useToggleDisplayModal();

    return (
        <li className={styles['sort-by']} ref={containerRef}>
            <span onClick={toggleDisplayModal}>sort by</span>
            <ChevronToggle
                onToggle={toggleDisplayModal}
                isOpen={displayModal}
            />

            {displayModal && (
                <span className={styles['menu']}>
                    <button>Best Rating</button>
                    <button>Available Now</button>
                    <button>Price: Low to High</button>
                    <button>Price: High to Low</button>
                </span>
            )}
        </li>
    );
};
