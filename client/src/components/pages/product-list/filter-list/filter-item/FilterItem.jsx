import { ChevronToggle } from '../../../../reusable/chevron-toggle/ChevronToggle';
import { Button } from './button/Button';

import { useCategoryName } from '../../../../../hooks/useCategoryName';
import { useFilterToggle } from '../../../../../hooks/useFilterToggle';

import { useProductFiltersContext } from '../../../../../contexts/ProductFiltersContext';

import styles from './FilterItem.module.scss';

export const FilterItem = ({ label, data }) => {
    const { filterToggleFunctions, filtersMapper } = useProductFiltersContext();
    const { categoryName } = useCategoryName();

    const { displayFilter, toggleDisplayFilter, contentRef, animationStyles } = useFilterToggle(
        data,
        categoryName
    );

    const handleFilterToggle = itemId => {
        filterToggleFunctions[label](itemId);
    };

    return (
        <li className={styles['filter-item']}>
            <div className={styles['label-wrapper']}>
                <h6 onClick={toggleDisplayFilter}>{label}</h6>
                <ChevronToggle isOpen={displayFilter} onToggle={toggleDisplayFilter} />
            </div>

            <ul ref={contentRef} className={styles['list']} style={animationStyles}>
                {data.map(item => (
                    <Button
                        key={item.id}
                        item={item}
                        label={label}
                        isSelected={filtersMapper[label].includes(item.id)}
                        onToggle={handleFilterToggle}
                    />
                ))}
            </ul>
        </li>
    );
};
