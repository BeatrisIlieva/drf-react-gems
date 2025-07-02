import { useState, useEffect, useRef } from 'react';
import styles from './AddressFormModal.module.scss';

export const Dropdown = ({ 
    value, 
    onChange, 
    options = [], 
    placeholder, 
    loading = false, 
    error = false,
    onOpen 
}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [dropUp, setDropUp] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    useEffect(() => {
        if (isOpen && dropdownRef.current) {
            const rect = dropdownRef.current.getBoundingClientRect();
            const spaceBelow = window.innerHeight - rect.bottom;
            const spaceAbove = rect.top;
            const menuHeight = 192; // max-height of dropdown menu (12rem)

            setDropUp(spaceBelow < menuHeight && spaceAbove > menuHeight);
        }
    }, [isOpen]);

    const handleToggle = () => {
        const willOpen = !isOpen;
        
        if (willOpen && onOpen) {
            onOpen();
        }
        setIsOpen(willOpen);
    };

    const handleSelect = (option) => {
        onChange(option);
        setIsOpen(false);
    };

    const selectedOption = options.find(opt => opt.value === value);

    return (
        <div className={styles.dropdown} ref={dropdownRef}>
            <button
                type="button"
                className={`${styles.dropdownToggle} ${error ? styles.error : ''}`}
                onClick={handleToggle}
            >
                <span className={selectedOption ? '' : styles.placeholder}>
                    {selectedOption ? selectedOption.label : placeholder}
                </span>
                <span className={`${styles.arrow} ${isOpen ? styles.open : ''}`}></span>
            </button>

            {isOpen && (
                <div className={`${styles.dropdownMenu} ${dropUp ? styles.dropUp : ''}`}>
                    {loading ? (
                        <div className={styles.loadingItem}>Loading...</div>
                    ) : options.length > 0 ? (
                        options.map((option) => (
                            <div
                                key={option.value}
                                className={`${styles.dropdownItem} ${
                                    option.value === value ? styles.selected : ''
                                }`}
                                onClick={() => handleSelect(option)}
                            >
                                {option.label}
                            </div>
                        ))
                    ) : (
                        <div className={styles.noResults}>No options available</div>
                    )}
                </div>
            )}
        </div>
    );
};
