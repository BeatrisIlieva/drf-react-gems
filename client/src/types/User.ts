export interface UserData {
  id?: string;
  _id?: string;
  email?: string;
  refresh?: string;
  access?: string;
}

export interface UserContextType extends UserData {
  userLoginHandler: (resultData: UserData) => void;
  userLogoutHandler: () => void;
}

export interface FormFieldState {
  value: string;
  error: string;
  valid: boolean;
}

export interface UserFormData {
  email: FormFieldState;
  password: FormFieldState;
  password_confirmation?: FormFieldState;
  firstName?: FormFieldState;
  lastName?: FormFieldState;
  phoneNumber?: FormFieldState;
  [key: string]: FormFieldState | undefined;
}
