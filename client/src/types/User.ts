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

// Generic form data interface that can accommodate any field combination
export interface FormData {
  [key: string]: FormFieldState | undefined;
}

// Specific form interfaces extending the generic one
export interface UserFormData extends FormData {
  email: FormFieldState;
  username?: FormFieldState;
  password: FormFieldState;
  password_confirmation?: FormFieldState;
  firstName?: FormFieldState;
  lastName?: FormFieldState;
  phoneNumber?: FormFieldState;
  currentPassword?: FormFieldState;
  newPassword?: FormFieldState;
}

export interface LoginFormData extends FormData {
  email_or_username: FormFieldState;
  password: FormFieldState;
}

export interface RegisterFormData extends FormData {
  email: FormFieldState;
  username: FormFieldState;
  password: FormFieldState;
}

// Action state for form submissions
export interface FormActionState<T = unknown> {
  success?: boolean;
  error?: string;
  data?: T;
}

// Form submission result
export interface FormSubmissionResult<T = unknown> {
  success: boolean;
  error?: string;
  data?: T;
}
