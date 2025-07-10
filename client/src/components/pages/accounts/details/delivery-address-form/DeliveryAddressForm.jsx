import { Button } from '../../../../reusable/button/Button';
import { FormFieldRenderer } from '../../../../reusable/form-field-renderer/FormFieldRenderer';
import { ShadowBox } from '../../../../reusable/shadow-box/ShadowBox';

import { useDeliveryForm } from '../../../../../hooks/useDeliveryForm';

import styles from './DeliveryAddressForm.module.scss';

export const DeliveryAddressForm = ({
    buttonTitle = 'Save',
    buttonGrow = '0',
    showButton = true,
    onSubmit: externalOnSubmit,
    onFormReady,
}) => {
    const { formProps, fieldConfig, loading } = useDeliveryForm(externalOnSubmit, onFormReady);

    const {
        formData,
        validateField,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting,
        formRef,
        registerInput,
    } = formProps;

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
