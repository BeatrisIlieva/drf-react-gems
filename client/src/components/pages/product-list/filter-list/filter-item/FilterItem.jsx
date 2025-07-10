// import { useEffect, useRef, useState } from 'react';
// import { ChevronToggle } from '../../../../reusable/chevron-toggle/ChevronToggle';
// import { Icon } from '../../../../reusable/icon/Icon';
// import { useCategoryName } from '../../../../../hooks/useCategoryName';
// import { useProductFiltersContext } from '../../../../../contexts/ProductFiltersContext';
// import styles from './FilterItem.module.scss';
// export const FilterItem = ({ label, data }) => {
//     const { filterToggleFunctions, filtersMapper } = useProductFiltersContext();
//     const { categoryName } = useCategoryName();
//     const [displayFilter, setDisplayFilter] = useState(false);
//     const toggleDisplayFilter = () => {
//         setDisplayFilter(() => !displayFilter);
//     };
//     const [height, setHeight] = useState(0);
//     const contentRef = useRef(null);
//     useEffect(() => {
//         if (displayFilter && contentRef.current) {
//             const scrollHeight = contentRef.current.scrollHeight;
//             setHeight(scrollHeight);
//         } else {
//             setHeight(0);
//         }
//     }, [displayFilter, data, contentRef]);
//     useEffect(() => {
//         setDisplayFilter(false);
//     }, [categoryName]);
//     const clickHandler = itemId => {
//         filterToggleFunctions[label](itemId);
//     };
//     return (
//         <li className={styles['filter-item']}>
//             <div className={styles['label-wrapper']}>
//                 <h6 onClick={toggleDisplayFilter}>{label}</h6>
//                 <ChevronToggle isOpen={displayFilter} onToggle={toggleDisplayFilter} />
//             </div>
//             <ul
//                 ref={contentRef}
//                 className={styles['list']}
//                 style={{
//                     maxHeight: height,
//                     opacity: displayFilter ? 1 : 0,
//                     overflow: 'hidden',
//                     transition: 'max-height 0.3s ease, opacity 0.3s ease',
//                     marginTop: displayFilter ? '1em' : '0',
//                 }}
//             >
//                 {data.map(item => (
//                     <li
//                         key={item.id}
//                         className={`${
//                             filtersMapper[label].includes(item.id) ? styles['selected'] : ''
//                         }`.trim()}
//                     >
//                         <button
//                             disabled={filtersMapper[label].includes(item.id)}
//                             className={styles['add-filter']}
//                             onClick={() => clickHandler(item.id)}
//                         >
//                             {item.hex && (
//                                 <span
//                                     className={`${styles['visualization']} ${
//                                         item.label === 'White' ? styles['white'] : ''
//                                     }`.trim()}
//                                     style={{
//                                         backgroundColor: item.hex,
//                                     }}
//                                 ></span>
//                             )}
//                             {item.image && (
//                                 <span className={styles['visualization']}>
//                                     <img src={item.image} alt={item.label} />
//                                 </span>
//                             )}
//                             <span>{item.label}</span>
//                             <span className={styles['count']}>({item.count})</span>
//                         </button>
//                         {filtersMapper[label].includes(item.id) && (
//                             <div
//                                 className={styles['remove-filter']}
//                                 onClick={() => clickHandler(item.id)}
//                             >
//                                 <Icon name={'xMark'} isSubtle={true} fontSize={0.7} />
//                             </div>
//                         )}
//                     </li>
//                 ))}
//             </ul>
//         </li>
//     );
// };
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
