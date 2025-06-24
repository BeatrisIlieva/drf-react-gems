export interface UserContextType {
    id: string;
    email: string;
    refresh: string;
    access: string;
    userLoginHandler: (data: UserContextPayload) => void;
    userLogoutHandler: () => void;
}

export type UserContextPayload = Omit<
    UserContextType,
    'userLoginHandler' | 'userLogoutHandler'
>;
