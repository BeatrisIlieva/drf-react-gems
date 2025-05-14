import { useContext } from 'react';
import useUserContext, { UserContext } from '../../../contexts/UserContext';
import { useDelete } from '../../../api/authApi';

export const Delete = () => {
    const { refresh, access } = useContext(UserContext);
    const { deleteUser } = useDelete();

    const { userLogoutHandler } = useUserContext();

    const deleteHandler = async () => {
        const data = { refresh, access };

        try {
            await deleteUser(data);

            userLogoutHandler();
        } catch (err) {
            console.log(err.message);
        }
    };

    return (
        <button type='submit' onClick={deleteHandler}>
            Delete
        </button>
    );
};
