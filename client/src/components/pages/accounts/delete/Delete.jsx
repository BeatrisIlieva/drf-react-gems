import { useDelete } from '../../../../api/authApi';

import { useUserContext } from '../../../../contexts/UserContext';

export const Delete = () => {
    const { deleteUser } = useDelete();
    const { userLogoutHandler } = useUserContext();

    const deleteHandler = async () => {
        try {
            await deleteUser();
            userLogoutHandler();
        } catch (err) {
            console.error(err instanceof Error ? err.message : String(err));
        }
    };

    return (
        <button type="submit" onClick={deleteHandler}>
            Delete
        </button>
    );
};
