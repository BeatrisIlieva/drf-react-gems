import { useEffect, useRef, useState } from 'react';

export const useFilterToggle = (data, categoryName) => {
    const [displayFilter, setDisplayFilter] = useState(false);
    const [height, setHeight] = useState(0);
    const contentRef = useRef(null);

    const toggleDisplayFilter = () => {
        setDisplayFilter(prev => !prev);
    };

    useEffect(() => {
        if (displayFilter && contentRef.current) {
            const scrollHeight = contentRef.current.scrollHeight;
            setHeight(scrollHeight);
        } else {
            setHeight(0);
        }
    }, [displayFilter, data]);

    useEffect(() => {
        setDisplayFilter(false);
    }, [categoryName]);

    const getAnimationStyles = () => ({
        maxHeight: height,
        opacity: displayFilter ? 1 : 0,
        overflow: 'hidden',
        transition: 'max-height 0.3s ease, opacity 0.3s ease',
        marginTop: displayFilter ? '1em' : '0',
    });

    return {
        displayFilter,
        toggleDisplayFilter,
        contentRef,
        animationStyles: getAnimationStyles(),
    };
};
