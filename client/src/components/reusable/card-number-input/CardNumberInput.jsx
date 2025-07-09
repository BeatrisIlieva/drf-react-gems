import { useEffect, useRef, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCcVisa, faCcMastercard } from "@fortawesome/free-brands-svg-icons";
import { getFieldDisplayName } from "../../../utils/getFieldDisplayName";

import styles from "./CardNumberInput.module.scss";

export const CardNumberInput = ({
    fieldName,
    fieldData,
    handleFieldChange,
    validateField,
    registerInput,
    fieldConfig,
    getInputClassName,
}) => {
    const inputRef = useRef(null);
    const [cardType, setCardType] = useState(null);

    const config = fieldConfig?.[fieldName] || {};
    const required = config.required !== false;
    const maxLength = config.maxLength || 19;

    const formatCardNumber = (value) => {
        const digitsOnly = value.replace(/\D/g, "");

        const limitedDigits = digitsOnly.substring(0, 16);

        let formattedValue = "";
        for (let i = 0; i < limitedDigits.length; i++) {
            if (i > 0 && i % 4 === 0) {
                formattedValue += " ";
            }
            formattedValue += limitedDigits[i];
        }

        return formattedValue;
    };

    const detectCardType = (value) => {
        const cleanValue = value.replace(/\s/g, "");

        if (cleanValue.length < 1) {
            setCardType(null);
            return;
        }

        if (cleanValue.startsWith("4")) {
            setCardType("visa");
            return;
        }

        if (cleanValue.length >= 2) {
            const firstTwo = cleanValue.substring(0, 2);
            const firstTwoNum = parseInt(firstTwo, 10);

            if (firstTwoNum >= 51 && firstTwoNum <= 55) {
                setCardType("mastercard");
                return;
            }
        }

        if (cleanValue.length >= 4) {
            const firstFour = cleanValue.substring(0, 4);
            const firstFourNum = parseInt(firstFour, 10);

            if (firstFourNum >= 2221 && firstFourNum <= 2720) {
                setCardType("mastercard");
                return;
            }
        }

        setCardType(null);
    };

    const handleInputChange = (e) => {
        const input = inputRef.current;
        const rawValue = e.target.value;
        const cursorPosition = input ? input.selectionStart : 0;

        const formattedValue = formatCardNumber(rawValue);

        detectCardType(formattedValue);

        const syntheticEvent = {
            target: {
                name: fieldName,
                value: formattedValue,
            },
        };

        handleFieldChange(syntheticEvent);

        if (input) {
            setTimeout(() => {
                if (document.activeElement === input) {
                    let digitsBeforeCursor = 0;
                    for (
                        let i = 0;
                        i < Math.min(cursorPosition, rawValue.length);
                        i++
                    ) {
                        if (/\d/.test(rawValue[i])) {
                            digitsBeforeCursor++;
                        }
                    }

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

                    if (digitCount < digitsBeforeCursor) {
                        newCursorPosition = formattedValue.length;
                    }

                    newCursorPosition = Math.max(
                        0,
                        Math.min(newCursorPosition, formattedValue.length),
                    );

                    input.setSelectionRange(
                        newCursorPosition,
                        newCursorPosition,
                    );
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
        if (cardType === "visa") {
            return (
                <FontAwesomeIcon
                    icon={faCcVisa}
                    className={styles["card-icon"]}
                />
            );
        }
        if (cardType === "mastercard") {
            return (
                <FontAwesomeIcon
                    icon={faCcMastercard}
                    className={styles["card-icon"]}
                />
            );
        }
        return null;
    };

    return (
        <div className={`field ${styles["card-number-field"]}`}>
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
                maxLength={maxLength}
            />
            <label htmlFor={fieldName} className={getInputClassName(fieldData)}>
                {getFieldDisplayName(fieldName)}
                {required ? "*" : ""}
            </label>
            {getCardIcon()}
            {fieldData.error && (
                <span className="error">{fieldData.error}</span>
            )}
        </div>
    );
};
