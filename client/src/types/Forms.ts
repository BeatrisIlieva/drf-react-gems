export interface FormField {
    value: string;
    error: string;
    valid: boolean;
}

export interface CustomFormData {
    [key: string]: FormField;
}
