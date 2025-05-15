import { useEffect } from 'react';

export function useFocusOnInvalidInput() {
    useEffect(() => {
        const handleInvalid = (e) => {
            e.preventDefault();

            const invalidElements = document.querySelectorAll('input:invalid');

            if (invalidElements.length > 0) {
                const firstInvalid = invalidElements[0];
                firstInvalid.focus();
            }
        };

        document.addEventListener('invalid', handleInvalid, true);

        return () => {
            document.removeEventListener('invalid', handleInvalid, true);
        };
    }, []);
}
