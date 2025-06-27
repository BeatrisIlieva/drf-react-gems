/**
 * Get a user-friendly display label for form field names
 * Following the principle of separation of concerns - this utility handles field name presentation
 */
export const getFieldDisplayName = (fieldName: string): string => {
    const fieldDisplayNames: Record<string, string> = {
        email_or_username: 'Email or Username',
        firstName: 'First Name',
        lastName: 'Last Name',
        phoneNumber: 'Phone Number',
        password_confirmation: 'Confirm Password'
    };

    return fieldDisplayNames[fieldName] || 
           fieldName.charAt(0).toUpperCase() + fieldName.slice(1);
};
