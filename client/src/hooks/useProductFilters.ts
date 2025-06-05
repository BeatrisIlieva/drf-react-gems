import { useEffect, useState } from 'react';

import { useCategoryName } from './useCategoryName';
import { useProductListContext } from '../contexts/ProductListContext';

export const useProductFilters = () => {
    const { categoryName } = useCategoryName();
    const { resetPage } = useProductListContext();

    const [colorIds, setColorIds] = useState<number[]>([]);
    const [stoneIds, setStoneIds] = useState<number[]>([]);
    const [metalIds, setMetalIds] = useState<number[]>([]);
    const [collectionIds, setCollectionIds] = useState<number[]>([]);
    const [priceIds, setPriceIds] = useState<string[]>([]);

    const [displayFilters, setDisplayFilters] = useState<boolean>(false);

    useEffect(() => {
        setColorIds([]);
        setStoneIds([]);
        setMetalIds([]);
        setCollectionIds([]);
        setPriceIds([]);
    }, [categoryName]);

    const toggleDisplayFilters = () => {
        setDisplayFilters(() => !displayFilters);
    };

    type EntityName = 'collection' | 'color' | 'metal' | 'stone' | 'price';

    const entityMapper: Record<EntityName, (id: number | string) => void> = {
        collection: (id) =>
            setCollectionIds((prev) =>
                prev.includes(id as number)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as number]
            ),
        color: (id) =>
            setColorIds((prev) =>
                prev.includes(id as number)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as number]
            ),
        metal: (id) =>
            setMetalIds((prev) =>
                prev.includes(id as number)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as number]
            ),
        stone: (id) =>
            setStoneIds((prev) =>
                prev.includes(id as number)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as number]
            ),
        price: (id) =>
            setPriceIds((prev) =>
                prev.includes(id as string)
                    ? prev.filter((i) => i !== id)
                    : [...prev, id as string]
            )
    };

    function updateEntityCharacteristics(
        entityName: 'Collection' | 'Color' | 'Metal' | 'Price' | 'Stone',
        entityId: number | string
    ): void {
        resetPage();
        entityMapper[entityName.toLowerCase() as keyof typeof entityMapper](entityId);
    }

    const entityStateMapper = {
        Color: colorIds,
        Stone: stoneIds,
        Metal: metalIds,
        Collection: collectionIds,
        Price: priceIds
    };

    useEffect(() => {
        setDisplayFilters(false);
    }, [categoryName]);

    return {
        toggleDisplayFilters,
        updateEntityCharacteristics,
        displayFilters,
        entityStateMapper,
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        priceIds
    };
};
