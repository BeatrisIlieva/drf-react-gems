import { useRef, useCallback } from "react";

export function useFocusOnInvalidInput() {
    const formRef = useRef(null);
    const inputRefs = useRef(new Map());

    const registerInput = useCallback((name, ref) => {
        if (ref) {
            inputRefs.current.set(name, ref);
        } else {
            inputRefs.current.delete(name);
        }
    }, []);

    const focusFirstInvalid = useCallback((formData) => {
        if (!formData) return false;

        for (const [fieldName, fieldValue] of Object.entries(formData)) {
            if (fieldValue.error) {
                const inputRef = inputRefs.current.get(fieldName);
                if (inputRef) {
                    inputRef.focus();
                    return true;
                }
            }
        }
        return false;
    }, []);

    return {
        formRef,
        registerInput,
        focusFirstInvalid,
    };
}
