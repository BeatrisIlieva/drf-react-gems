import { useEffect } from 'react';

export function useFocusOnInvalidInput(): void {
    useEffect(() => {
        const handleInvalid = (e: Event) => {
            e.preventDefault();

            const invalidElements = document.querySelectorAll('input:invalid');

            if (invalidElements.length > 0) {
                const firstInvalid = invalidElements[0] as HTMLElement;
                firstInvalid.focus();
            }
        };

        document.addEventListener('invalid', handleInvalid, true);

        return () => {
            document.removeEventListener('invalid', handleInvalid, true);
        };
    }, []);
}
