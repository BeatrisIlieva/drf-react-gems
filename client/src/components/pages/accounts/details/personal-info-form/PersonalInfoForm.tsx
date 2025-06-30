import { Fragment, useState, useEffect } from 'react';
import { useForm } from '../../../../../hooks/useForm';
import { useFocusOnInvalidInput } from '../../../../../hooks/useFocusOnInvalidInput';
import { useGetPersonalInfo, useUpdatePersonalInfo } from '../../../../../api/authApi';
import { InputField } from '../../../../reusable/input-field/InputField';
import { Button } from '../../../../reusable/button/Button';
import { keysToSnakeCase } from '../../../../../utils/convertToSnakeCase';
import { keysToCamelCase } from '../../../../../utils/convertToCamelCase';

import styles from './PersonalInfoForm.module.scss';
import type { ReactElement } from 'react';
import type { UserFormData } from '../../../../../types/User';

// Simple useActionState alternative for form submission
interface ActionState<T> {
    status: 'idle' | 'pending' | 'success' | 'error';
    data?: T;
    error?: Error;
}

type ActionFunction<T> = () => Promise<T>;

function useActionState<T>(
    action: ActionFunction<T>
): [ActionState<T>, () => Promise<T>, boolean] {
    const [state, setState] = useState<ActionState<T>>({
        status: 'idle'
    });

    const actionFn = async () => {
        setState({ status: 'pending' });
        try {
            const result = await action();
            setState({ status: 'success', data: result });
            return result;
        } catch (error) {
            const err =
                error instanceof Error
                    ? error
                    : new Error(String(error));
            setState({ status: 'error', error: err });
            throw err;
        }
    };

    const isPending = state.status === 'pending';

    return [state, actionFn, isPending];
}

export const PersonalInfoForm = (): ReactElement => {
    const initialFormValues: UserFormData = {
        email: { value: '', error: '', valid: false }, // Required by UserFormData
        password: { value: '', error: '', valid: false }, // Required by UserFormData
        firstName: { value: '', error: '', valid: false },
        lastName: { value: '', error: '', valid: false },
        phoneNumber: { value: '', error: '', valid: false }
    };

    const {
        userData,
        validateField,
        handleFieldChange,
        setServerSideError,
        getInputClassName
    } = useForm(initialFormValues);

    const { getPersonalInfo } = useGetPersonalInfo();
    const { updatePersonalInfo } = useUpdatePersonalInfo();

    useFocusOnInvalidInput();

    const [loading, setLoading] = useState(true);
    const [successMessage, setSuccessMessage] = useState<string | null>(null);
    const [initialData, setInitialData] = useState<Record<string, string>>({});

    // Load existing personal info on component mount
    useEffect(() => {
        const loadPersonalInfo = async () => {
            try {
                const personalInfo = await getPersonalInfo();
                if (personalInfo) {
                    const camelCaseInfo = keysToCamelCase(personalInfo);
                    setInitialData(camelCaseInfo);
                }
            } catch (error) {
                console.error('Failed to load personal info:', error);
            } finally {
                setLoading(false);
            }
        };

        loadPersonalInfo();
    }, [getPersonalInfo]);

    // Update form fields when initial data is loaded
    useEffect(() => {
        if (Object.keys(initialData).length > 0) {
            Object.entries(initialData).forEach(([key, value]) => {
                if (userData[key] && typeof value === 'string') {
                    userData[key] = {
                        value: value,
                        error: '',
                        valid: true
                    };
                }
            });
        }
    }, [initialData, userData]);

    const submitHandler = async () => {
        setSuccessMessage(null);
        
        // Only validate the personal info fields (not email/password)
        const personalInfoData = {
            firstName: userData.firstName!,
            lastName: userData.lastName!,
            phoneNumber: userData.phoneNumber!
        };

        // Custom validation for personal info fields
        let isValid = true;
        const validatedUserData = { ...personalInfoData };

        Object.entries(personalInfoData).forEach(([field, fieldData]) => {
            if (!fieldData) return;
            
            // Skip validation if field is empty (optional fields)
            if (fieldData.value.trim() === '') {
                validatedUserData[field as keyof typeof validatedUserData] = {
                    ...fieldData,
                    error: '',
                    valid: true
                };
                return;
            }

            const errorMessage = fieldData.error;
            if (errorMessage !== '') {
                isValid = false;
            }

            validatedUserData[field as keyof typeof validatedUserData] = {
                ...fieldData,
                valid: errorMessage === ''
            };
        });

        if (!isValid) {
            return { success: false, error: 'Validation failed' };
        }

        // Prepare data for API (convert to snake_case and only include non-empty values)
        const apiData: Record<string, string> = {};
        Object.entries(validatedUserData).forEach(([key, fieldData]) => {
            if (fieldData && fieldData.value && fieldData.value.trim() !== '') {
                apiData[key] = fieldData.value.trim();
            }
        });

        const snakeCaseData = keysToSnakeCase(apiData) as Record<string, string>;

        const result = await updatePersonalInfo(snakeCaseData);

        if (result && !result.error) {
            setSuccessMessage('Personal information updated successfully!');
            return { success: true };
        }

        // Handle server-side errors
        if (result && typeof result === 'object') {
            const camelCaseErrors = keysToCamelCase(result);
            Object.keys(personalInfoData).forEach((key) => {
                setServerSideError(
                    camelCaseErrors as Record<string, string[]>,
                    key
                );
            });
        }

        return { success: false };
    };

    const [, submitAction, isPending] = useActionState(submitHandler);

    if (loading) {
        return <div className={styles.loading}>Loading personal information...</div>;
    }

    // Only render the personal info fields (not email/password)
    const personalInfoFields = ['firstName', 'lastName', 'phoneNumber'];

    return (
        <section className={styles['personal-info-form']}>
            <h2>Personal Information</h2>
            
            {successMessage && (
                <div className={styles['success-message']}>
                    {successMessage}
                </div>
            )}

            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    submitAction();
                }}
            >
                {personalInfoFields.map((fieldName) => {
                    const fieldData = userData[fieldName];
                    if (!fieldData) return null;

                    return (
                        <Fragment key={fieldName}>
                            <InputField
                                getInputClassName={getInputClassName}
                                fieldData={fieldData}
                                handleFieldChange={handleFieldChange}
                                validateField={validateField}
                                fieldName={fieldName}
                                type="text"
                            />
                        </Fragment>
                    );
                })}

                <Button
                    title="Save Changes"
                    color="black"
                    actionType="submit"
                    pending={isPending}
                    callbackHandler={() => {}}
                />
            </form>
        </section>
    );
};
