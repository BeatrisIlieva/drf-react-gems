import { useCallback, useState } from 'react';

export default function usePersistedState(
    stateKey,
    initialState
) {
    const [state, setState] = useState(() => {
        const persistedState = localStorage.getItem(stateKey);
        if (!persistedState) {
            return typeof initialState === 'function'
                ? initialState()
                : initialState;
        }

        const persistedStateData = JSON.parse(persistedState);

        return persistedStateData;
    });

    const setPersistedState = useCallback(
        (input) => {
            const data =
                typeof input === 'function'
                    ? input(state)
                    : input;

            const persistedData = JSON.stringify(data);

            localStorage.setItem(stateKey, persistedData);

            setState(data);
        },
        [state, stateKey]
    );

    return [state, setPersistedState];
}
