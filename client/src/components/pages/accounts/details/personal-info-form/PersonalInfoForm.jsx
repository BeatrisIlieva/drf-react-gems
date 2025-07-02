import { Fragment, useState, useEffect, useMemo } from 'react';
import { useForm } from '../../../../../hooks/useForm';
import { useProfile } from '../../../../../api/accounts/useProfileApi';
import { InputField } from '../../../../reusable/input-field/InputField';
import { Button } from '../../../../reusable/button/Button';
import { DetailsContainer } from '../details-container/DetailsContainer';
import { keysToCamelCase } from '../../../../../utils/convertToCamelCase';

import styles from './PersonalInfoForm.module.scss';

export const PersonalInfoForm = () => {
    const initialFormValues = useMemo(
        () => ({
            firstName: { value: '', error: '', valid: false },
            lastName: { value: '', error: '', valid: false },
            phoneNumber: { value: '', error: '', valid: false }
        }),
        []
    );

    const { getPersonalInfo, updatePersonalInfo } = useProfile();

    const [loading, setLoading] = useState(true);
    const [initialDataLoaded, setInitialDataLoaded] =
        useState(false);

    const formProps = useForm(initialFormValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: false
    });

    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting,
        handleServerSideErrors,
        updateFieldValue,
        validateFields,
        resetValidationStates,
        formRef,
        registerInput
    } = formProps;

    async function handleSubmit(formData) {
        const hasFirstName =
            formData.firstName?.value?.trim() !== '';
        const hasLastName =
            formData.lastName?.value?.trim() !== '';
        const hasPhoneNumber =
            formData.phoneNumber?.value?.trim() !== '';

        if (!hasFirstName || !hasLastName || !hasPhoneNumber) {
            validateFields();
            return {
                success: false,
                error: 'Please fill in all required fields.'
            };
        }

        const apiData = {
            first_name: formData.firstName.value.trim(),
            last_name: formData.lastName.value.trim(),
            phone_number: formData.phoneNumber.value.trim()
        };

        try {
            const result = await updatePersonalInfo(apiData);

            if (result && !result.error) {
                return { success: true };
            }

            // Handle server-side errors
            if (result && typeof result === 'object') {
                handleServerSideErrors(result);
            }

            return {
                success: false,
                error: 'Failed to update personal information'
            };
        } catch (error) {
            console.error('API error:', error);
            return {
                success: false,
                error: 'Failed to update personal information'
            };
        }
    }

    // Load existing personal info on component mount
    useEffect(() => {
        if (initialDataLoaded) return;

        const loadPersonalInfo = async () => {
            try {
                const personalInfo = await getPersonalInfo();
                if (personalInfo) {
                    const camelCaseInfo =
                        keysToCamelCase(personalInfo);

                    // Use updateFieldValue to populate without marking as valid initially
                    if (camelCaseInfo.firstName) {
                        updateFieldValue(
                            'firstName',
                            camelCaseInfo.firstName,
                            false
                        );
                    }
                    if (camelCaseInfo.lastName) {
                        updateFieldValue(
                            'lastName',
                            camelCaseInfo.lastName,
                            false
                        );
                    }
                    if (camelCaseInfo.phoneNumber) {
                        updateFieldValue(
                            'phoneNumber',
                            camelCaseInfo.phoneNumber,
                            false
                        );
                    }
                }
                setInitialDataLoaded(true);
            } finally {
                setLoading(false);
            }
        };

        loadPersonalInfo();
    }, [getPersonalInfo, updateFieldValue, initialDataLoaded]);

    // Handle server-side errors after form submission
    useEffect(() => {
        if (
            formProps.formState &&
            !formProps.formState.success &&
            formProps.formState.data
        ) {
            handleServerSideErrors(formProps.formState.data);
        }
    }, [formProps.formState, handleServerSideErrors]);

    // Handle successful form submission - reset validation states
    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    return (
        <DetailsContainer>
            <h3>Personal Information</h3>

            {loading ? (
                <div className={styles['loading']}>
                    Loading personal information...
                </div>
            ) : (
                <form ref={formRef} action={submitAction}>
                    {['firstName', 'lastName', 'phoneNumber'].map(
                        (fieldName) => {
                            const fieldData = formData[fieldName];
                            if (!fieldData) return null;

                            return (
                                <Fragment key={fieldName}>
                                    <InputField
                                        getInputClassName={
                                            getInputClassName
                                        }
                                        fieldData={fieldData}
                                        handleFieldChange={
                                            handleFieldChange
                                        }
                                        validateField={
                                            validateField
                                        }
                                        fieldName={fieldName}
                                        type='text'
                                        registerInput={
                                            registerInput
                                        }
                                    />
                                </Fragment>
                            );
                        }
                    )}

                    <Button
                        title='Save'
                        color='black'
                        actionType='submit'
                        pending={isSubmitting}
                        callbackHandler={() => {}}
                    />
                </form>
            )}
        </DetailsContainer>
    );
};
