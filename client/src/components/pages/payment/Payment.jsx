import { useEffect, useCallback } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCcVisa, faCcMastercard } from '@fortawesome/free-brands-svg-icons';
import { useForm } from '../../../hooks/useForm';
import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';
import { Button } from '../../reusable/button/Button';
import { ShadowBox } from '../../reusable/shadow-box/ShadowBox';
import { InputField } from '../../reusable/input-field/InputField';
import { CardNumberInput } from '../../reusable/card-number-input/CardNumberInput';
import { FORM_CONFIGS } from '../../../config/formFieldConfigs';
import { createApiDataFromForm } from '../../../utils/formHelpers';
import { formatPrice } from '../../../utils/formatPrice';

import styles from './Payment.module.scss';

export const Payment = () => {
    const { fieldConfig, initialValues } = FORM_CONFIGS.payment;
    const { shoppingBagTotalPrice } = useShoppingBagContext();

    const handleSubmit = useCallback(
        async (formData) => {
            const apiData = createApiDataFromForm(formData, fieldConfig);

            try {
                // Here you would call your payment API
                console.log('Processing payment with data:', apiData);
                
                // Simulate API call
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                return { success: true };
            } catch {
                return {
                    success: false,
                    error: 'Payment processing failed'
                };
            }
        },
        [fieldConfig]
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
        resetValidationStates,
        formRef,
        registerInput
    } = formProps;

    // Handle successful form submission - reset validation states
    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    const renderField = (fieldName) => {
        const fieldData = formData[fieldName];
        const config = fieldConfig[fieldName] || {};
        
        if (!fieldData) return null;

        if (fieldName === 'cardNumber') {
            return (
                <CardNumberInput
                    key={fieldName}
                    fieldName={fieldName}
                    fieldData={fieldData}
                    handleFieldChange={handleFieldChange}
                    validateField={validateField}
                    registerInput={registerInput}
                    fieldConfig={fieldConfig}
                    getInputClassName={getInputClassName}
                />
            );
        }

        return (
            <InputField
                key={fieldName}
                getInputClassName={getInputClassName}
                fieldData={fieldData}
                handleFieldChange={handleFieldChange}
                validateField={validateField}
                fieldName={fieldName}
                type={config.type || 'text'}
                registerInput={registerInput}
                fieldConfig={fieldConfig}
            />
        );
    };

    return (
        <ShadowBox title="Payment">
            <fieldset className={styles['payment-fieldset']}>
                <legend className={styles['payment-legend']}>
                    <span>Card Details</span>
                    <span className={styles['card-icons']}>
                        <FontAwesomeIcon icon={faCcMastercard} />
                        <FontAwesomeIcon icon={faCcVisa} />
                    </span>
                </legend>
                
                <form
                    ref={formRef}
                    action={submitAction}
                    className={styles['payment-form']}
                >
                    {Object.keys(fieldConfig).map(fieldName => renderField(fieldName))}

                    <Button
                        title={`Place Order ${formatPrice(shoppingBagTotalPrice || 3800)}`}
                        color='black'
                        actionType='submit'
                        pending={isSubmitting}
                        success={formProps.formState?.success}
                        callbackHandler={() => {}}
                        buttonGrow='1'
                    />
                </form>
            </fieldset>
        </ShadowBox>
    );
};