import { useEffect, useRef, useState } from 'react';

export const useToggleDisplayModal = () => {
    const [displayModal, setDisplayModal] = useState(false);

    const containerRef = useRef<HTMLLIElement | null>(null);

    const toggleDisplayModal = () => {
        setDisplayModal((prev) => !prev);
    };

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (
                containerRef.current &&
                !containerRef.current.contains(event.target as Node)
            ) {
                setDisplayModal(false);
            }
        };

        if (displayModal) {
            document.addEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [displayModal]);

    return {
        displayModal,
        containerRef,
        toggleDisplayModal
    };
};
