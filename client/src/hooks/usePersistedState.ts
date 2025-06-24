import { useCallback, useState } from "react";

type SetStateAction<T> = T | ((prevState: T) => T);

export default function usePersistedState<T>(stateKey: string, initialState: T | (() => T)): [T, (value: SetStateAction<T>) => void] {
    const [state, setState] = useState<T>(() => {
        const persistedState = localStorage.getItem(stateKey);
        if (!persistedState) {
            return typeof initialState === 'function' 
                ? (initialState as () => T)() 
                : initialState;
        }

        const persistedStateData = JSON.parse(persistedState);

        return persistedStateData as T;
    });

    const setPersistedState = useCallback((input: SetStateAction<T>) => {
        const data = typeof input === 'function' 
            ? (input as (prevState: T) => T)(state) 
            : input;

        const persistedData = JSON.stringify(data);

        localStorage.setItem(stateKey, persistedData);

        setState(data);
    }, [state, stateKey]);

    return [
        state,
        setPersistedState,
    ]
}
