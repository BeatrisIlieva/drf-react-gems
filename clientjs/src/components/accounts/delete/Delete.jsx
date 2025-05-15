import useUserContext from '../../../contexts/UserContext';
import { useDelete } from '../../../api/authApi';

export const Delete = () => {
    const { deleteUser } = useDelete();

    const { userLogoutHandler } = useUserContext();

    const deleteHandler = async () => {
        try {
            await deleteUser();

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
