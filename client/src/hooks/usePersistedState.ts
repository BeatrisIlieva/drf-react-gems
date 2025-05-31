import { useCallback, useState } from 'react';
import type { Dispatch, SetStateAction } from 'react';

export const usePersistedState = <T>(
    stateKey: string,
    initialState: T | (() => T)
): [T, Dispatch<SetStateAction<T>>] => {
    const [state, setState] = useState<T>(() => {
        const persistedState = localStorage.getItem(stateKey);
        if (!persistedState) {
            return typeof initialState === 'function'
                ? (initialState as () => T)()
                : initialState;
        }

        try {
            return JSON.parse(persistedState) as T;
        } catch {
            return typeof initialState === 'function'
                ? (initialState as () => T)()
                : initialState;
        }
    });

    const setPersistedState: Dispatch<SetStateAction<T>> = useCallback(
        (input) => {
            const data =
                typeof input === 'function'
                    ? (input as (prev: T) => T)(state)
                    : input;

            localStorage.setItem(stateKey, JSON.stringify(data));
            setState(data);
        },
        [state, stateKey]
    );

    return [state, setPersistedState];
};
