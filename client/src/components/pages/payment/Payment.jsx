import { useCallback, useEffect } from 'react';

import { useNavigate } from 'react-router';

import { faCcMastercard, faCcVisa } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { Button } from '../../reusable/button/Button';
import { CardNumberInput } from '../../reusable/card-number-input/CardNumberInput';
import { Delivery } from '../../reusable/delivery/Delivery';
import { InputField } from '../../reusable/input-field/InputField';
import { OrderSummary } from '../../reusable/order-summary/OrderSummary';
import { PaddedContainer } from '../../reusable/padded-container/PaddedContainer';
import { ProductsSummaryList } from '../../reusable/products-summary-list/ProductsSummaryList';
import { ShadowBox } from '../../reusable/shadow-box/ShadowBox';
import { ShippingInformation } from './shipping-information/ShippingInformation';

import { useOrder } from '../../../api/orderApi';

import { useForm } from '../../../hooks/useForm';

import { useShoppingBagContext } from '../../../contexts/ShoppingBagContext';

import { createApiDataFromForm } from '../../../utils/formHelpers';
import { formatPrice } from '../../../utils/formatPrice';
import { formatCardNumber, formatCvv, formatExpiryDate } from '../../../utils/paymentValidation';

import { FORM_CONFIGS } from '../../../config/formFieldConfigs';

import styles from './Payment.module.scss';

export const Payment = () => {
    const { fieldConfig, initialValues } = FORM_CONFIGS.payment;
    const { shoppingBagTotalPrice, refreshShoppingBag, shoppingBagItems } = useShoppingBagContext();
    const { createOrderFromBag } = useOrder();

    const navigate = useNavigate();

    const handleSubmit = useCallback(
        async formData => {
            const apiData = createApiDataFromForm(formData, fieldConfig);

            try {
                const result = await createOrderFromBag(apiData);

                if (result && !result.error) {
                    await refreshShoppingBag();
                    navigate('/user/order-confirmation');
                    return {
                        success: true,
                        data: result,
                    };
                }

                if (result && typeof result === 'object') {
                    return {
                        success: false,
                        data: result,
                    };
                }
            } catch (error) {
                return {
                    success: false,
                    error: error.response?.data || 'Failed to process payment',
                };
            }
        },
        [fieldConfig, createOrderFromBag, refreshShoppingBag]
    );

    const formProps = useForm(initialValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true,
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
        registerInput,
    } = formProps;

    const handleFormattedFieldChange = useCallback(
        (fieldName, value) => {
            let formattedValue = value;

            switch (fieldName) {
                case 'cardNumber':
                    formattedValue = formatCardNumber(value);
                    break;
                case 'expiryDate':
                    formattedValue = formatExpiryDate(value);
                    break;
                case 'cvv':
                    formattedValue = formatCvv(value);
                    break;
                default:
                    break;
            }

            handleFieldChange(fieldName, formattedValue);
        },
        [handleFieldChange]
    );

    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    const renderField = fieldName => {
        const fieldData = formData[fieldName];
        const config = fieldConfig[fieldName] || {};

        if (!fieldData) return null;

        if (fieldName === 'cardNumber') {
            return (
                <CardNumberInput
                    key={fieldName}
                    fieldName={fieldName}
                    fieldData={fieldData}
                    handleFieldChange={handleFormattedFieldChange}
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
                handleFieldChange={handleFormattedFieldChange}
                validateField={validateField}
                fieldName={fieldName}
                type={config.type || 'text'}
                registerInput={registerInput}
                fieldConfig={fieldConfig}
            />
        );
    };

    return (
        <PaddedContainer backgroundColor="lightest-grey">
            <section className={styles['checkout']}>
                <div className={styles['wrapper-left']}>
                    <ShippingInformation />
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
                                    title={`Place Order ${formatPrice(shoppingBagTotalPrice)}`}
                                    color="black"
                                    actionType="submit"
                                    pending={isSubmitting}
                                    success={formProps.formState?.success}
                                    callbackHandler={() => {}}
                                    buttonGrow="1"
                                />
                            </form>
                        </fieldset>
                    </ShadowBox>
                </div>

                <OrderSummary>
                    <ProductsSummaryList products={shoppingBagItems}>
                        <Delivery fontSize={1} />
                    </ProductsSummaryList>
                </OrderSummary>
            </section>
        </PaddedContainer>
    );
};
