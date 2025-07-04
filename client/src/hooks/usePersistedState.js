import { useCallback, useState } from 'react';

export default function usePersistedState(
    stateKey,
    initialState
) {
    const [state, setState] = useState(() => {
        const persistedState = localStorage.getItem(stateKey);
        if (!persistedState || persistedState === 'undefined') {
            return typeof initialState === 'function'
                ? initialState()
                : initialState;
        }

        try {
            const persistedStateData = JSON.parse(persistedState);
            return persistedStateData;
        } catch {
            // If JSON parsing fails, remove the invalid data and use initial state
            localStorage.removeItem(stateKey);
            return typeof initialState === 'function'
                ? initialState()
                : initialState;
        }
    });

    const setPersistedState = useCallback(
        (input) => {
            setState((prevState) => {
                const data =
                    typeof input === 'function'
                        ? input(prevState)
                        : input;

                const persistedData = JSON.stringify(data);

                localStorage.setItem(stateKey, persistedData);

                return data;
            });
        },
        [stateKey]
    );

    return [state, setPersistedState];
}
