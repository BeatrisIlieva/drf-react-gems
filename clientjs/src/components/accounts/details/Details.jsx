import { Logout } from '../logout/Logout';
import { useEffect, useState } from 'react';
import { useDetail } from '../../../api/authApi';

import { Delete } from '../delete/Delete';

export const Details = () => {
    const [user, setUser] = useState([]);
    const { detail } = useDetail();

    useEffect(() => {
        detail().then((response) => setUser(response));
    }, [detail]);

    return (
        <>
            <Logout />
            <Delete />
        </>
    );
};
