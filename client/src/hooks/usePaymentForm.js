import { useCallback, useEffect } from 'react';

import { useNavigate } from 'react-router';

import { useForm } from './useForm';

import { useOrder } from '../api/orderApi';

import { useShoppingBagContext } from '../contexts/ShoppingBagContext';

import { createApiDataFromForm } from '../utils/formHelpers';

import { FORM_CONFIGS } from '../config/formFieldConfigs';

export const usePaymentForm = () => {
    const { refreshShoppingBag } = useShoppingBagContext();
    const { createOrderFromBag } = useOrder();
    const navigate = useNavigate();

    const { fieldConfig, initialValues } = FORM_CONFIGS.payment;

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
        [fieldConfig, createOrderFromBag, refreshShoppingBag, navigate]
    );

    const formProps = useForm(initialValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true,
    });

    const { resetValidationStates } = formProps;

    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    return {
        formProps,
        fieldConfig,
    };
};
