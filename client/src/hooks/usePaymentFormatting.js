import { useCallback } from 'react';

import { formatCardNumber, formatCvv, formatExpiryDate } from '../utils/paymentValidation';

export const usePaymentFormatting = handleFieldChange => {
    const handleFormattedFieldChange = useCallback(
        (fieldName, value) => {
            let formattedValue = value;

            switch (fieldName) {
                case 'cardNumber':
                    formattedValue = formatCardNumber(value);
                    break;
                case 'expiryDate':
                    formattedValue = formatExpiryDate(value);
                    break;
                case 'cvv':
                    formattedValue = formatCvv(value);
                    break;
                default:
                    break;
            }

            handleFieldChange(fieldName, formattedValue);
        },
        [handleFieldChange]
    );

    return { handleFormattedFieldChange };
};
