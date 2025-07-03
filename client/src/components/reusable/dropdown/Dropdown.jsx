import { useState, useEffect, useRef } from 'react';
import styles from './Dropdown.module.scss';
import { ChevronToggle } from '../chevron-toggle/ChevronToggle';

export const Dropdown = ({
    value,
    onChange,
    options = [],
    loading = false,
    onOpen,
    fieldName,
    getInputClassName,
    fieldData,
    fieldConfig,
    label,
    noOptionsMessage = 'No options available'
}) => {
    const [isOpen, setIsOpen] = useState(false);
    const [dropUp, setDropUp] = useState(false);
    const dropdownRef = useRef(null);

    useEffect(() => {
        const handleClickOutside = (event) => {
            if (
                dropdownRef.current &&
                !dropdownRef.current.contains(event.target)
            ) {
                setIsOpen(false);
            }
        };

        document.addEventListener(
            'mousedown',
            handleClickOutside
        );
        return () =>
            document.removeEventListener(
                'mousedown',
                handleClickOutside
            );
    }, []);

    useEffect(() => {
        if (isOpen && dropdownRef.current) {
            const rect =
                dropdownRef.current.getBoundingClientRect();
            const spaceBelow = window.innerHeight - rect.bottom;
            const spaceAbove = rect.top;
            const menuHeight = 12 * 16; // 12rem in pixels

            if (
                spaceBelow < menuHeight &&
                spaceAbove > menuHeight
            ) {
                setDropUp(true);
            } else {
                setDropUp(false);
            }
        }
    }, [isOpen]);

    const handleToggle = () => {
        if (!isOpen && onOpen) {
            onOpen();
        }
        setIsOpen(!isOpen);
    };

    const handleOptionSelect = (option) => {
        onChange(option);
        setIsOpen(false);
    };

    const selectedOption = options.find(
        (opt) => opt.id === value
    );

    // If we have a value but no matching option (e.g., during initial load),
    // show a loading placeholder instead of an empty value
    const displayValue = selectedOption
        ? selectedOption.name ||
          selectedOption.streetAddress ||
          selectedOption.zipCode
        : value && !loading && options.length === 0
        ? 'Loading...'
        : '';

    const inputClassName = fieldData
        ? getInputClassName(fieldData)
        : '';

    const dropdownClasses = `${styles.dropdown} ${
        inputClassName === 'valid' ? styles.valid : ''
    } ${inputClassName === 'invalid' ? styles.invalid : ''} ${
        isOpen ? styles.open : ''
    } ${displayValue ? styles.hasValue : ''}`;

    // Create a placeholder value for the hidden input to trigger floating label
    // When dropdown has value or is open, use a space to trigger :not(:placeholder-shown)
    const hiddenInputValue = displayValue ? ' ' : '';

    return (
        <div className='field' ref={dropdownRef}>
            {/* Hidden input to work with forms.scss floating label logic */}
            <input
                onClick={handleToggle}
                type='text'
                id={fieldName}
                value={hiddenInputValue}
                placeholder=' '
                readOnly
                style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: '100%',
                    opacity: 0,
                    zIndex: -1
                }}
                className={inputClassName}
            />

            <div
                className={dropdownClasses}
                onClick={handleToggle}
            >
                <span className={styles.value}>
                    {displayValue || ''}
                </span>
                <ChevronToggle isOpen={isOpen} />
            </div>

            {label && (
                <label
                    htmlFor={fieldName}
                    className={inputClassName}
                >
                    {label}
                    {fieldData &&
                    fieldConfig &&
                    fieldConfig[fieldName]?.required
                        ? '*'
                        : ''}
                </label>
            )}

            {isOpen && (
                <div
                    className={`${styles.menu} ${
                        dropUp ? styles.dropUp : styles.dropDown
                    }`}
                >
                    {loading ? (
                        <div className={styles.loading}>
                            Loading...
                        </div>
                    ) : options.length > 0 ? (
                        options.map((option) => (
                            <div
                                key={option.id}
                                className={`${styles.option} ${
                                    option.id === value
                                        ? styles.selected
                                        : ''
                                }`}
                                onMouseDown={() =>
                                    handleOptionSelect(option)
                                }
                            >
                                {option.name ||
                                    option.streetAddress ||
                                    option.zipCode}
                            </div>
                        ))
                    ) : (
                        <div className={styles.noOptions}>
                            {noOptionsMessage}
                        </div>
                    )}
                </div>
            )}

            {fieldData?.error && (
                <span className='error'>{fieldData.error}</span>
            )}
        </div>
    );
};
