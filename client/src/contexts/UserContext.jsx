import { createContext, useContext } from "react";

export const UserContext = createContext({
    id: "",
    email: "",
    username: "",
    refresh: "",
    access: "",
    userLoginHandler: () => null,
    userLogoutHandler: () => null,
});

export const useUserContext = () => {
    const data = useContext(UserContext);

    return data;
};
