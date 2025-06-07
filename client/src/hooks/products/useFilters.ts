import { useCallback, useMemo, useState } from 'react';
import type { EntityName } from '../../types/ProductList';
import { toggleIdInArray } from '../../utils/toggleIdInArray';

export const useFilters = () => {
    const [colorIds, setColorIds] = useState<number[]>([]);
    const [stoneIds, setStoneIds] = useState<number[]>([]);
    const [metalIds, setMetalIds] = useState<number[]>([]);
    const [collectionIds, setCollectionIds] = useState<number[]>([]);
    const [displayFilters, setDisplayFilters] = useState(false);

    const filtersMapper = useMemo(
        () => ({
            Color: colorIds,
            Stone: stoneIds,
            Metal: metalIds,
            Collection: collectionIds
        }),
        [colorIds, stoneIds, metalIds, collectionIds]
    );

    const toggleDisplayFilters = useCallback(() => {
        setDisplayFilters((prev) => !prev);
    }, []);

    const filterToggleFunctions = useMemo<
        Record<EntityName, (id: number | string) => void>
    >(
        () => ({
            Collection: (id) =>
                setCollectionIds((prev) => toggleIdInArray(prev, id as number)),
            Color: (id) => setColorIds((prev) => toggleIdInArray(prev, id as number)),
            Metal: (id) => setMetalIds((prev) => toggleIdInArray(prev, id as number)),
            Stone: (id) => setStoneIds((prev) => toggleIdInArray(prev, id as number))
        }),
        []
    );

    const updateFilterByEntity = useCallback(
        (entityName: EntityName, entityId: number | string) => {
            filterToggleFunctions[entityName](entityId);
        },
        [filterToggleFunctions]
    );

    const resetFilters = useCallback(() => {
        setColorIds([]);
        setStoneIds([]);
        setMetalIds([]);
        setCollectionIds([]);
        setDisplayFilters(false);
    }, []);

    return {
        colorIds,
        stoneIds,
        metalIds,
        collectionIds,
        displayFilters,
        filtersMapper,
        toggleDisplayFilters,
        updateFilterByEntity,
        resetFilters
    };
};
