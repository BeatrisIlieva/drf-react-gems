import { useCallback, useEffect } from 'react';

import { Button } from '../../../../reusable/button/Button';
import { FormFieldRenderer } from '../../../../reusable/form-field-renderer/FormFieldRenderer';
import { ShadowBox } from '../../../../reusable/shadow-box/ShadowBox';

import { useProfile } from '../../../../../api/useProfileApi';

import { useForm } from '../../../../../hooks/useForm';
import { useFormDataLoader } from '../../../../../hooks/useFormDataLoader';

import { createApiDataFromForm } from '../../../../../utils/formHelpers';

import { FORM_CONFIGS } from '../../../../../config/formFieldConfigs';

import styles from './DeliveryAddressForm.module.scss';

export const DeliveryAddressForm = ({
    buttonTitle = 'Save',
    buttonGrow = '0',
    showButton = true,
    onSubmit: externalOnSubmit,
    onFormReady,
}) => {
    const { fieldConfig, initialValues } = FORM_CONFIGS.deliveryAddress;
    const { getPersonalInfo, updatePersonalInfo } = useProfile();

    const handleSubmit = useCallback(
        async formData => {
            const apiData = createApiDataFromForm(formData, fieldConfig);

            try {
                const result = await updatePersonalInfo(apiData);

                if (result && !result.error) {
                    return { success: true };
                }

                if (result && typeof result === 'object') {
                    return {
                        success: false,
                        data: result,
                    };
                }
            } catch {
                return {
                    success: false,
                    error: 'Failed to update delivery information',
                };
            }
        },
        [fieldConfig, updatePersonalInfo]
    );

    const formProps = useForm(initialValues, {
        onSubmit: externalOnSubmit || handleSubmit,
        validateOnSubmit: true,
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
        registerInput,
    } = formProps;

    const { loading } = useFormDataLoader(getPersonalInfo, updateFieldValue, fieldConfig);

    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    useEffect(() => {
        if (onFormReady) {
            onFormReady({
                submitAction,
                formState: formProps.formState,
            });
        }
    }, [submitAction, formProps.formState, onFormReady]);

    const fieldNames = Object.keys(fieldConfig);

    return (
        <ShadowBox title="Delivery Information">
            {loading ? (
                <div className={styles['loading']}>Loading delivery information...</div>
            ) : (
                <form ref={formRef} action={submitAction} className={styles['delivery-form']}>
                    <FormFieldRenderer
                        fieldNames={fieldNames}
                        formData={formData}
                        getInputClassName={getInputClassName}
                        handleFieldChange={handleFieldChange}
                        validateField={validateField}
                        registerInput={registerInput}
                        fieldConfig={fieldConfig}
                    />

                    {showButton && (
                        <Button
                            title={buttonTitle}
                            color="black"
                            actionType="submit"
                            pending={isSubmitting}
                            success={formProps.formState?.success}
                            callbackHandler={() => {}}
                            buttonGrow={buttonGrow}
                            width="5"
                        />
                    )}
                </form>
            )}
        </ShadowBox>
    );
};
