export const PAYMENT_CONSTANTS = {
    CARD_PREFIXES: {
        VISA: "4",
        MASTERCARD_51: "51",
        MASTERCARD_55: "55",
        MASTERCARD_222: "222",
        MASTERCARD_227: "227",
        MASTERCARD_27: "27",
    },

    CARD_PATTERNS: {
        VISA: "^4[0-9]{3} [0-9]{4} [0-9]{4} [0-9]{4}$",
        MASTERCARD_LEGACY: "^5[1-5][0-9]{2} [0-9]{4} [0-9]{4} [0-9]{4}$",
        MASTERCARD_NEW:
            "^(222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720) [0-9]{4} [0-9]{4} [0-9]{4}$",
    },

    CVV_PATTERN: "^[0-9]{3}$",

    EXPIRY_DATE_PATTERN: "^(0[1-9]|1[0-2])/([0-9]{2})$",

    CARD_HOLDER_PATTERN: "^[A-Za-z\\u00C0-\\u024F'\\- ]{2,50}$",

    ERRORS: {
        CARD_NUMBER: "Please enter a valid card number",
        CARD_HOLDER: "Please enter a valid name",
        CVV: "Please enter a valid security code",
        EXPIRY_DATE: "Please enter a valid expiry date (MM/YY)",
        EXPIRED_CARD: "Card has expired",
    },
};
