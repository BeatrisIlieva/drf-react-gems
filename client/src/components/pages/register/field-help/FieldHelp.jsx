const FIELD_HELP_TEXT = {
    email: 'Enter your email for important order updates.',
    username: 'Choose a unique username for your account.',
};

export const FieldHelp = ({ fieldName, show }) => {
    const helpText = FIELD_HELP_TEXT[fieldName];

    if (!show || !helpText) return null;

    return <p>{helpText}</p>;
};
