import { useEffect, useCallback } from 'react';
import { useForm } from '../../../../../hooks/useForm';
import { useProfile } from '../../../../../api/accounts/useProfileApi';
import { useFormDataLoader } from '../../../../../hooks/useFormDataLoader';
import { FormFieldRenderer } from '../../../../common/FormFieldRenderer';
import { Button } from '../../../../reusable/button/Button';
import { ShadowBox } from '../../../../reusable/shadow-box/ShadowBox';
import { FORM_CONFIGS } from '../../../../../config/formFieldConfigs';
import { createApiDataFromForm } from '../../../../../utils/formHelpers';

import styles from './PersonalInfoForm.module.scss';

export const PersonalInfoForm = () => {
    const { fieldConfig, initialValues } =
        FORM_CONFIGS.personalInfo;
    const { getPersonalInfo, updatePersonalInfo } = useProfile();

    const handleSubmit = useCallback(
        async (formData) => {
            const apiData = createApiDataFromForm(
                formData,
                fieldConfig
            );

            try {
                const result = await updatePersonalInfo(apiData);

                if (result && !result.error) {
                    return { success: true };
                }

                if (result && typeof result === 'object') {
                    return {
                        success: false,
                        data: result
                    };
                }
            } catch {
                return {
                    success: false,
                    error: 'Failed to update personal information'
                };
            }
        },
        [fieldConfig, updatePersonalInfo]
    );

    const formProps = useForm(initialValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true
    });

    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting,
        updateFieldValue,
        resetValidationStates,
        formRef,
        registerInput
    } = formProps;

    const { loading } = useFormDataLoader(
        getPersonalInfo,
        updateFieldValue,
        fieldConfig
    );

    // Handle successful form submission - reset validation states
    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    const fieldNames = Object.keys(fieldConfig);

    return (
        <ShadowBox title='Personal Information'>
            {loading ? (
                <div className={styles['loading']}>
                    Loading personal information...
                </div>
            ) : (
                <form
                    ref={formRef}
                    action={submitAction}
                    className={styles['personal-info-form']}
                >
                    <FormFieldRenderer
                        fieldNames={fieldNames}
                        formData={formData}
                        getInputClassName={getInputClassName}
                        handleFieldChange={handleFieldChange}
                        validateField={validateField}
                        registerInput={registerInput}
                        fieldConfig={fieldConfig}
                    />

                    <Button
                        title='Save'
                        color='black'
                        actionType='submit'
                        pending={isSubmitting}
                        success={formProps.formState?.success}
                        callbackHandler={() => {}}
                        buttonGrow='0'
                        width='5'
                    />
                </form>
            )}
        </ShadowBox>
    );
};
