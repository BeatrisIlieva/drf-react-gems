import { useEffect, useRef, useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCcVisa, faCcMastercard } from '@fortawesome/free-brands-svg-icons';
import { getFieldDisplayName } from '../../../utils/getFieldDisplayName';
import { PAYMENT_CONSTANTS } from '../../../constants/paymentConstants';

import styles from './CardNumberInput.module.scss';

export const CardNumberInput = ({
    fieldName,
    fieldData,
    handleFieldChange,
    validateField,
    registerInput,
    fieldConfig,
    getInputClassName
}) => {
    const inputRef = useRef(null);
    const [cardType, setCardType] = useState(null);

    const config = fieldConfig?.[fieldName] || {};
    const required = config.required !== false;
    const maxLength = config.maxLength || 19;

    const paymentCardsMapper = {
        [PAYMENT_CONSTANTS.CARD_PREFIXES.VISA]: {
            type: 'visa'
        },
        [PAYMENT_CONSTANTS.CARD_PREFIXES.MASTERCARD_51]: {
            type: 'mastercard'
        },
        [PAYMENT_CONSTANTS.CARD_PREFIXES.MASTERCARD_55]: {
            type: 'mastercard'
        },
        [PAYMENT_CONSTANTS.CARD_PREFIXES.MASTERCARD_222]: {
            type: 'mastercard'
        },
        [PAYMENT_CONSTANTS.CARD_PREFIXES.MASTERCARD_227]: {
            type: 'mastercard'
        },
        [PAYMENT_CONSTANTS.CARD_PREFIXES.MASTERCARD_27]: {
            type: 'mastercard'
        }
    };

    const formatCardNumber = (value) => {
        // Remove all non-digits
        const digitsOnly = value.replace(/\D/g, '');
        
        // Limit to 16 digits maximum
        const limitedDigits = digitsOnly.substring(0, 16);
        
        // Add spaces every 4 digits
        let formattedValue = '';
        for (let i = 0; i < limitedDigits.length; i++) {
            if (i > 0 && i % 4 === 0) {
                formattedValue += ' ';
            }
            formattedValue += limitedDigits[i];
        }
        
        return formattedValue;
    };

    const detectCardType = (value) => {
        const cleanValue = value.replace(/\s/g, '');
        
        const firstDigit = cleanValue[0];
        const firstTwoDigits = cleanValue.substring(0, 2);
        const firstThreeDigits = cleanValue.substring(0, 3);

        let detectedType = null;

        if (paymentCardsMapper[firstDigit]) {
            detectedType = paymentCardsMapper[firstDigit].type;
        } else if (paymentCardsMapper[firstTwoDigits]) {
            detectedType = paymentCardsMapper[firstTwoDigits].type;
        } else if (paymentCardsMapper[firstThreeDigits]) {
            detectedType = paymentCardsMapper[firstThreeDigits].type;
        }

        setCardType(detectedType);
    };

    const handleInputChange = (e) => {
        const input = inputRef.current;
        const rawValue = e.target.value;
        const cursorPosition = input ? input.selectionStart : 0;
        
        // Format the card number
        const formattedValue = formatCardNumber(rawValue);
        
        // Detect card type
        detectCardType(formattedValue);
        
        // Create synthetic event with formatted value
        const syntheticEvent = {
            target: {
                name: fieldName,
                value: formattedValue
            }
        };

        // Call the parent handler first
        handleFieldChange(syntheticEvent);

        // Calculate new cursor position based on the change
        if (input) {
            setTimeout(() => {
                if (document.activeElement === input) {
                    // Count digits before cursor position in the raw input
                    let digitsBeforeCursor = 0;
                    for (let i = 0; i < Math.min(cursorPosition, rawValue.length); i++) {
                        if (/\d/.test(rawValue[i])) {
                            digitsBeforeCursor++;
                        }
                    }
                    
                    // Find the position in formatted string that corresponds to this digit count
                    let newCursorPosition = 0;
                    let digitCount = 0;
                    
                    for (let i = 0; i < formattedValue.length; i++) {
                        if (/\d/.test(formattedValue[i])) {
                            digitCount++;
                            if (digitCount === digitsBeforeCursor) {
                                newCursorPosition = i + 1;
                                break;
                            }
                        }
                    }
                    
                    // If we haven't found the position yet, place cursor at the end
                    if (digitCount < digitsBeforeCursor) {
                        newCursorPosition = formattedValue.length;
                    }
                    
                    // Ensure cursor position is within bounds
                    newCursorPosition = Math.max(0, Math.min(newCursorPosition, formattedValue.length));
                    
                    input.setSelectionRange(newCursorPosition, newCursorPosition);
                }
            }, 0);
        }
    };

    const handleBlur = (e) => {
        if (validateField) {
            validateField(e);
        }
    };

    useEffect(() => {
        if (registerInput && inputRef.current) {
            registerInput(fieldName, inputRef.current);
        }
        return () => {
            if (registerInput && fieldName) {
                registerInput(fieldName, null);
            }
        };
    }, [registerInput, fieldName]);

    const getCardIcon = () => {
        if (cardType === 'visa') {
            return <FontAwesomeIcon icon={faCcVisa} className={styles['card-icon']} />;
        }
        if (cardType === 'mastercard') {
            return <FontAwesomeIcon icon={faCcMastercard} className={styles['card-icon']} />;
        }
        return null;
    };

    return (
        <div className={`field ${styles['card-number-field']}`}>
            <input
                ref={inputRef}
                className={getInputClassName(fieldData)}
                type="text"
                name={fieldName}
                id={fieldName}
                placeholder={fieldName}
                value={fieldData.value}
                onChange={handleInputChange}
                onBlur={handleBlur}
                required={required}
                maxLength={maxLength}
            />
            <label
                htmlFor={fieldName}
                className={getInputClassName(fieldData)}
            >
                {getFieldDisplayName(fieldName)}
                {required ? '*' : ''}
            </label>
            {getCardIcon()}
            {fieldData.error && (
                <span className='error'>{fieldData.error}</span>
            )}
        </div>
    );
};
