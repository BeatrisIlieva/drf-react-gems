import { useEffect, useCallback, useState } from 'react';
import { useForm } from '../../../../../hooks/useForm';
import { useUserAddress } from '../../../../../api/accounts/userAddressApi';
import { Dropdown } from '../../../../reusable/dropdown/Dropdown';
import { InputField } from '../../../../reusable/input-field/InputField';
import { Button } from '../../../../reusable/button/Button';
import { Icon } from '../../../../reusable/icon/Icon';
import { DetailsContainer } from '../details-container/DetailsContainer';
import { AddressDropdownGroup } from './components/AddressDropdownGroup';
import { FORM_CONFIGS } from '../../../../../config/formFieldConfigs';

import styles from './DeliveryAddressForm.module.scss';

export const DeliveryAddressForm = () => {
    const { fieldConfig, initialValues } =
        FORM_CONFIGS.deliveryAddress;
    const {
        getUserAddress,
        updateUserAddress,
        getStates,
        getCities,
        getZipCodes,
        getStreetAddresses
    } = useUserAddress();

    const [stateOptions, setStateOptions] = useState([]);
    const [cityOptions, setCityOptions] = useState([]);
    const [zipCodeOptions, setZipCodeOptions] = useState([]);
    const [streetAddressOptions, setStreetAddressOptions] =
        useState([]);
    const [loadingStates, setLoadingStates] = useState({
        states: false,
        cities: false,
        zipCodes: false,
        streetAddresses: false
    });

    const handleSubmit = useCallback(
        async (formData) => {
            // Check only required fields
            const requiredFields = Object.keys(
                fieldConfig
            ).filter(
                (fieldName) => fieldConfig[fieldName].required
            );

            const missingRequired = requiredFields.filter(
                (fieldName) => !formData[fieldName]?.value
            );

            if (missingRequired.length > 0) {
                return {
                    success: false,
                    error: 'Please fill in all required fields'
                };
            }

            const apiData = {};

            Object.keys(formData).forEach((fieldName) => {
                const field = fieldConfig[fieldName];
                const value = formData[fieldName]?.value;

                if (field) {
                    if (fieldName === 'apartment') {
                        apiData[field.apiKey] = value || '';
                    } else if (value) {
                        apiData[field.apiKey] = value;
                    }
                }
            });

            try {
                const result = await updateUserAddress(apiData);

                if (result && !result.error) {
                    return { success: true };
                }

                if (result && typeof result === 'object') {
                    return {
                        success: false,
                        data: result
                    };
                }

                return {
                    success: false,
                    error: 'Failed to update delivery address'
                };
            } catch {
                return {
                    success: false,
                    error: 'Failed to update delivery address'
                };
            }
        },
        [fieldConfig, updateUserAddress]
    );

    const customValidation = useCallback((fieldName, value) => {
        const field = fieldConfig[fieldName];
        if (!field) return '';

        // Only validate required fields
        if (field.required && (!value || value === '')) {
            return 'This field is required';
        }

        return '';
    }, [fieldConfig]);

    const formProps = useForm(initialValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true,
        customValidation
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

    const [loading, setLoading] = useState(true);
    const [initialDataLoaded, setInitialDataLoaded] =
        useState(false);

    const loadInitialData = useCallback(async () => {
        if (initialDataLoaded) return;

        try {
            const data = await getUserAddress();
            if (data) {
                // Load the IDs for form submission but ensure dropdowns show proper values
                if (data.streetAddress || data.street_address) {
                    updateFieldValue(
                        'streetAddress',
                        data.streetAddress || data.street_address,
                        false
                    );
                }
                if (data.apartment) {
                    updateFieldValue(
                        'apartment',
                        data.apartment,
                        false
                    );
                }
                if (data.city) {
                    updateFieldValue('city', data.city, false);
                }
                if (data.state) {
                    updateFieldValue('state', data.state, false);
                }
                if (data.zipCode || data.zip_code) {
                    updateFieldValue(
                        'zipCode',
                        data.zipCode || data.zip_code,
                        false
                    );
                }
            }
            setInitialDataLoaded(true);
        } finally {
            setLoading(false);
        }
    }, [getUserAddress, updateFieldValue, initialDataLoaded]);

    useEffect(() => {
        loadInitialData();
    }, [loadInitialData]);

    const loadStates = useCallback(async () => {
        setLoadingStates((prev) => ({ ...prev, states: true }));
        try {
            const states = await getStates();
            setStateOptions(states || []);
        } catch {
            setStateOptions([]);
        } finally {
            setLoadingStates((prev) => ({
                ...prev,
                states: false
            }));
        }
    }, [getStates]);

    const loadCities = useCallback(
        async (stateId = null) => {
            setLoadingStates((prev) => ({
                ...prev,
                cities: true
            }));
            try {
                const cities = await getCities(stateId);
                setCityOptions(cities || []);
            } catch {
                setCityOptions([]);
            } finally {
                setLoadingStates((prev) => ({
                    ...prev,
                    cities: false
                }));
            }
        },
        [getCities]
    );

    const loadZipCodes = useCallback(
        async (cityId = null) => {
            setLoadingStates((prev) => ({
                ...prev,
                zipCodes: true
            }));
            try {
                const zipCodes = await getZipCodes(cityId);
                setZipCodeOptions(zipCodes || []);
            } catch {
                setZipCodeOptions([]);
            } finally {
                setLoadingStates((prev) => ({
                    ...prev,
                    zipCodes: false
                }));
            }
        },
        [getZipCodes]
    );

    const loadStreetAddresses = useCallback(
        async (zipCodeId = null) => {
            setLoadingStates((prev) => ({
                ...prev,
                streetAddresses: true
            }));
            try {
                const streetAddresses = await getStreetAddresses(
                    zipCodeId
                );
                setStreetAddressOptions(streetAddresses || []);
            } catch {
                setStreetAddressOptions([]);
            } finally {
                setLoadingStates((prev) => ({
                    ...prev,
                    streetAddresses: false
                }));
            }
        },
        [getStreetAddresses]
    );

    // Load dependent data when initial data is loaded
    useEffect(() => {
        if (initialDataLoaded) {
            const stateValue = formData.state.value;
            const cityValue = formData.city.value;
            const zipCodeValue = formData.zipCode.value;

            // Load states first
            if (stateValue || cityValue || zipCodeValue) {
                loadStates();
            }

            // Load cities if state is selected
            if (stateValue && (cityValue || zipCodeValue)) {
                loadCities(stateValue);
            }

            // Load zip codes if city is selected
            if (cityValue && zipCodeValue) {
                loadZipCodes(cityValue);
            }

            // Load street addresses if zip code is selected
            if (zipCodeValue) {
                loadStreetAddresses(zipCodeValue);
            }
        }
    }, [
        initialDataLoaded,
        formData.state.value,
        formData.city.value,
        formData.zipCode.value,
        loadStates,
        loadCities,
        loadZipCodes,
        loadStreetAddresses
    ]);

    const handleDropdownChange = useCallback(
        (fieldName, option) => {
            const value = option.id;
            
            // Simulate a field change event to trigger proper validation
            const syntheticEvent = {
                target: {
                    name: fieldName,
                    value: value
                }
            };
            
            // Use handleFieldChange to properly set validation states
            handleFieldChange(syntheticEvent);

            // Clear dependent fields and load their options
            if (fieldName === 'state') {
                updateFieldValue('city', '', false, true);
                updateFieldValue('zipCode', '', false, true);
                updateFieldValue('streetAddress', '', false, true);
                setCityOptions([]);
                setZipCodeOptions([]);
                setStreetAddressOptions([]);
                loadCities(option.id);
            } else if (fieldName === 'city') {
                updateFieldValue('zipCode', '', false, true);
                updateFieldValue('streetAddress', '', false, true);
                setZipCodeOptions([]);
                setStreetAddressOptions([]);
                loadZipCodes(option.id);
            } else if (fieldName === 'zipCode') {
                updateFieldValue('streetAddress', '', false, true);
                setStreetAddressOptions([]);
                loadStreetAddresses(option.id);
            }
        },
        [
            handleFieldChange,
            updateFieldValue,
            loadCities,
            loadZipCodes,
            loadStreetAddresses
        ]
    );

    useEffect(() => {
        if (formProps.formState && formProps.formState.success) {
            resetValidationStates();
        }
    }, [formProps.formState, resetValidationStates]);

    return (
        <DetailsContainer title='Delivery Information'>
            

            {loading ? (
                <div className={styles['loading']}>
                    Loading delivery information...
                </div>
            ) : (
                <form
                    ref={formRef}
                    action={submitAction}
                    className={styles['delivery-form']}
                >
                    <AddressDropdownGroup
                        formData={formData}
                        fieldConfig={fieldConfig}
                        stateOptions={stateOptions}
                        cityOptions={cityOptions}
                        zipCodeOptions={zipCodeOptions}
                        loadingStates={loadingStates}
                        loadStates={loadStates}
                        loadCities={loadCities}
                        loadZipCodes={loadZipCodes}
                        handleDropdownChange={
                            handleDropdownChange
                        }
                        getInputClassName={getInputClassName}
                    />

                    <div className='field'>
                        <Dropdown
                            value={formData.streetAddress.value}
                            onChange={(option) =>
                                handleDropdownChange(
                                    'streetAddress',
                                    option
                                )
                            }
                            options={streetAddressOptions}
                            placeholder='Street Address (No PO/APO/FPO)'
                            loading={
                                loadingStates.streetAddresses
                            }
                            onOpen={() => {
                                if (formData.zipCode.value) {
                                    loadStreetAddresses(
                                        formData.zipCode.value
                                    );
                                }
                            }}
                            fieldName='streetAddress'
                            getInputClassName={getInputClassName}
                            fieldData={formData.streetAddress}
                            fieldConfig={fieldConfig}
                            label={
                                fieldConfig.streetAddress.label
                            }
                            noOptionsMessage='Please select a ZIP Code'
                        />
                    </div>

                    <InputField
                        getInputClassName={getInputClassName}
                        fieldData={formData.apartment}
                        handleFieldChange={handleFieldChange}
                        validateField={validateField}
                        fieldName='apartment'
                        type='text'
                        registerInput={registerInput}
                    />

                    <div className={styles['country-field']}>
                        <input
                            type='text'
                            value='United States'
                            disabled
                            className={styles['country-input']}
                        />
                        <Icon name='lock' fontSize={0.7} />
                    </div>

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
