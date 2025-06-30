// Test file to verify the form fixes work correctly
import React from 'react';
import { useForm } from './hooks/useForm';
import type { UserFormData, FormSubmissionResult } from './types/User';

const TestForm: React.FC = () => {
    const initialFormValues: UserFormData = {
        email: { value: '', error: '', valid: false },
        password: { value: '', error: '', valid: false },
        firstName: { value: '', error: '', valid: false },
        lastName: { value: '', error: '', valid: false },
        phoneNumber: { value: '', error: '', valid: false }
    };

    const handleSubmit = async (formData: UserFormData): Promise<FormSubmissionResult> => {
        console.log('Form submitted:', formData);
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 1000));
        return { success: true };
    };

    const {
        formData,
        handleFieldChange,
        validateField,
        getInputClassName,
        submitAction,
        isSubmitting,
        interactedFields
    } = useForm(initialFormValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true
    });

    return (
        <div style={{ padding: '20px', maxWidth: '400px', margin: '0 auto' }}>
            <h2>Test Form - Verify Fixes</h2>
            <p>
                This form tests:
                <br />
                1. Fields should NOT be green/valid before user interaction
                <br />
                2. Form submission should work without useActionState warnings
                <br />
                3. Fields should only show valid state after user has interacted with them
            </p>
            
            <form action={submitAction}>
                {(['firstName', 'lastName', 'email'] as const).map((fieldName) => {
                    const fieldData = formData[fieldName];
                    const hasInteracted = interactedFields.has(fieldName);
                    
                    return (
                        <div key={fieldName} style={{ marginBottom: '15px' }}>
                            <label style={{ display: 'block', marginBottom: '5px' }}>
                                {fieldName.charAt(0).toUpperCase() + fieldName.slice(1)}
                                {hasInteracted && <span style={{ color: 'blue' }}> (interacted)</span>}
                            </label>
                            <input
                                name={fieldName}
                                value={fieldData?.value || ''}
                                onChange={handleFieldChange}
                                onBlur={validateField}
                                className={fieldData ? getInputClassName(fieldData) : ''}
                                style={{
                                    padding: '8px',
                                    border: '1px solid #ccc',
                                    borderRadius: '4px',
                                    width: '100%',
                                    backgroundColor: fieldData?.valid ? '#e8f5e8' : fieldData?.error ? '#ffe8e8' : 'white'
                                }}
                            />
                            {fieldData?.error && (
                                <div style={{ color: 'red', fontSize: '12px', marginTop: '2px' }}>
                                    {fieldData.error}
                                </div>
                            )}
                        </div>
                    );
                })}
                
                <button
                    type="submit"
                    disabled={isSubmitting}
                    style={{
                        padding: '10px 20px',
                        backgroundColor: '#007bff',
                        color: 'white',
                        border: 'none',
                        borderRadius: '4px',
                        cursor: isSubmitting ? 'not-allowed' : 'pointer'
                    }}
                >
                    {isSubmitting ? 'Submitting...' : 'Submit'}
                </button>
            </form>
        </div>
    );
};

export default TestForm;
