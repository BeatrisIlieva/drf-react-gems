export const getFieldDisplayName = (fieldName) => {
    const fieldDisplayNames = {
        email_or_username: 'Email or Username',
        firstName: 'First Name',
        lastName: 'Last Name',
        phoneNumber: 'Phone Number',
        password_confirmation: 'Confirm Password',
        currentPassword: 'Current Password',
        newPassword: 'New Password',
        apartment: 'Apartment/Suite/Floor (Optional)'
    };

    return (
        fieldDisplayNames[fieldName] ||
        fieldName.charAt(0).toUpperCase() + fieldName.slice(1)
    );
};
