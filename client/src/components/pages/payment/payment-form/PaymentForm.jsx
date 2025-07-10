import { faCcMastercard, faCcVisa } from '@fortawesome/free-brands-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';

import { Button } from '../../../reusable/button/Button';
import { ShadowBox } from '../../../reusable/shadow-box/ShadowBox';
import { PaymentField } from './payment-field/PaymentField';

import { usePaymentForm } from '../../../../hooks/usePaymentForm';
import { usePaymentFormatting } from '../../../../hooks/usePaymentFormatting';

import { useShoppingBagContext } from '../../../../contexts/ShoppingBagContext';

import { formatPrice } from '../../../../utils/formatPrice';

import styles from './PaymentForm.module.scss';

export const PaymentForm = () => {
    const { shoppingBagTotalPrice } = useShoppingBagContext();
    const { formProps, fieldConfig } = usePaymentForm();

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

    const { handleFormattedFieldChange } = usePaymentFormatting(handleFieldChange);

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

                <form ref={formRef} action={submitAction} className={styles['payment-form']}>
                    {Object.keys(fieldConfig).map(fieldName => (
                        <PaymentField
                            key={fieldName}
                            fieldName={fieldName}
                            fieldData={formData[fieldName]}
                            fieldConfig={fieldConfig}
                            handleFormattedFieldChange={handleFormattedFieldChange}
                            validateField={validateField}
                            registerInput={registerInput}
                            getInputClassName={getInputClassName}
                        />
                    ))}

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
    );
};
