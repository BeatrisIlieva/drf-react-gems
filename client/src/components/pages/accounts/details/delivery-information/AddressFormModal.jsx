import { useState, useEffect, useCallback, useRef } from 'react';
import { useForm } from '../../../../../hooks/useForm';
import { useUserAddress } from '../../../../../api/accounts/userAddressApi';
import { Popup } from '../../../../reusable/popup/Popup';
import { Dropdown } from './Dropdown';
import styles from './AddressFormModal.module.scss';

export const AddressFormModal = ({ isOpen, onClose, onSave }) => {
    const [stateOptions, setStateOptions] = useState([]);
    const [cityOptions, setCityOptions] = useState([]);
    const [zipCodeOptions, setZipCodeOptions] = useState([]);
    const [streetAddressOptions, setStreetAddressOptions] = useState([]);
    const [loadingStates, setLoadingStates] = useState({
        states: false,
        cities: false,
        zipCodes: false,
        streetAddresses: false
    });

    const { getStates, getCities, getZipCodes, getStreetAddresses, updateUserAddress } = useUserAddress();

    const prevStateRef = useRef();
    const prevCityRef = useRef();
    const prevZipCodeRef = useRef();

    const initialValues = {
        state: { value: '', error: '', valid: false },
        city: { value: '', error: '', valid: false },
        zipCode: { value: '', error: '', valid: false },
        streetAddress: { value: '', error: '', valid: false },
        apartment: { value: '', error: '', valid: true }
    };

    const handleSubmit = useCallback(async (formData) => {
        const apiData = {
            state: formData.state.value,
            city: formData.city.value,
            zipCode: formData.zipCode.value,
            streetAddress: formData.streetAddress.value,
            apartment: formData.apartment.value || null
        };

        try {
            const result = await updateUserAddress(apiData);

            if (result && !result.error) {
                onSave && onSave();
                onClose();
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
                error: 'Failed to save address information'
            };
        } catch {
            return {
                success: false,
                error: 'Failed to save address information'
            };
        }
    }, [updateUserAddress, onSave, onClose]);

    const formProps = useForm(initialValues, {
        onSubmit: handleSubmit,
        validateOnSubmit: true
    });

    const {
        formData,
        handleFieldChange,
        getInputClassName,
        submitAction,
        isSubmitting,
        formRef
    } = formProps;

    const loadStates = useCallback(async () => {
        setLoadingStates(prev => ({ ...prev, states: true }));
        try {
            const states = await getStates();
            if (states) {
                setStateOptions(states.map(state => ({
                    value: state.id,
                    label: state.name
                })));
            }
        } catch {
            setStateOptions([]);
        } finally {
            setLoadingStates(prev => ({ ...prev, states: false }));
        }
    }, [getStates]);

    const loadCities = useCallback(async (stateId) => {
        setLoadingStates(prev => ({ ...prev, cities: true }));
        try {
            const cities = await getCities(stateId);
            if (cities) {
                setCityOptions(cities.map(city => ({
                    value: city.id,
                    label: city.name
                })));
            }
        } catch {
            setCityOptions([]);
        } finally {
            setLoadingStates(prev => ({ ...prev, cities: false }));
        }
    }, [getCities]);

    const loadZipCodes = useCallback(async (cityId) => {
        setLoadingStates(prev => ({ ...prev, zipCodes: true }));
        try {
            const zipCodes = await getZipCodes(cityId);
            if (zipCodes) {
                setZipCodeOptions(zipCodes.map(zipCode => ({
                    value: zipCode.id,
                    label: zipCode.zipCode
                })));
            }
        } catch {
            setZipCodeOptions([]);
        } finally {
            setLoadingStates(prev => ({ ...prev, zipCodes: false }));
        }
    }, [getZipCodes]);

    const loadStreetAddresses = useCallback(async (zipCodeId) => {
        setLoadingStates(prev => ({ ...prev, streetAddresses: true }));
        try {
            const streetAddresses = await getStreetAddresses(zipCodeId);
            if (streetAddresses) {
                setStreetAddressOptions(streetAddresses.map(address => ({
                    value: address.id,
                    label: address.streetAddress
                })));
            }
        } catch {
            setStreetAddressOptions([]);
        } finally {
            setLoadingStates(prev => ({ ...prev, streetAddresses: false }));
        }
    }, [getStreetAddresses]);

    useEffect(() => {
        if (isOpen) {
            loadStates();
        }
    }, [isOpen, loadStates]);

    useEffect(() => {
        const currentState = formData.state.value;
        const prevState = prevStateRef.current;
        
        if (currentState !== prevState) {
            prevStateRef.current = currentState;
            
            if (currentState) {
                setCityOptions([]);
                setZipCodeOptions([]);
                setStreetAddressOptions([]);
                loadCities(currentState);
            } else {
                setCityOptions([]);
                setZipCodeOptions([]);
                setStreetAddressOptions([]);
            }
        }
    }, [formData.state.value, loadCities]);

    useEffect(() => {
        const currentCity = formData.city.value;
        const prevCity = prevCityRef.current;
        
        if (currentCity !== prevCity) {
            prevCityRef.current = currentCity;
            
            if (currentCity) {
                setZipCodeOptions([]);
                setStreetAddressOptions([]);
                loadZipCodes(currentCity);
            } else {
                setZipCodeOptions([]);
                setStreetAddressOptions([]);
            }
        }
    }, [formData.city.value, loadZipCodes]);

    useEffect(() => {
        const currentZipCode = formData.zipCode.value;
        const prevZipCode = prevZipCodeRef.current;
        
        if (currentZipCode !== prevZipCode) {
            prevZipCodeRef.current = currentZipCode;
            
            if (currentZipCode) {
                setStreetAddressOptions([]);
                loadStreetAddresses(currentZipCode);
            } else {
                setStreetAddressOptions([]);
            }
        }
    }, [formData.zipCode.value, loadStreetAddresses]);

    const handleDropdownChange = (fieldName, option) => {
        handleFieldChange(fieldName, option.value);
        
        if (fieldName === 'state') {
            handleFieldChange('city', '');
            handleFieldChange('zipCode', '');
            handleFieldChange('streetAddress', '');
        } else if (fieldName === 'city') {
            handleFieldChange('zipCode', '');
            handleFieldChange('streetAddress', '');
        } else if (fieldName === 'zipCode') {
            handleFieldChange('streetAddress', '');
        }
    };

    if (!isOpen) return null;

    return (
        <Popup isOpen={isOpen} onClose={onClose}>
            <div className={styles.modalContent}>
                <div className={styles.modalHeader}>
                    <h2>ADD A NEW ADDRESS</h2>
                </div>

                <form ref={formRef} action={submitAction} className={styles.form}>
                    <div className={styles.fieldGroup}>
                        <label htmlFor="streetAddress">Street Address *</label>
                        <Dropdown
                            value={formData.streetAddress.value}
                            onChange={(option) => handleDropdownChange('streetAddress', option)}
                            options={streetAddressOptions}
                            placeholder="Street Address *"
                            loading={loadingStates.streetAddresses}
                            error={!!formData.streetAddress.error}
                            onOpen={() => formData.zipCode.value && loadStreetAddresses(formData.zipCode.value)}
                        />
                        {formData.streetAddress.error && (
                            <div className={styles.errorMessage}>
                                {formData.streetAddress.error}
                            </div>
                        )}
                    </div>

                    <div className={styles.fieldGroup}>
                        <label htmlFor="apartment">Apartment/Suite #</label>
                        <input
                            type="text"
                            id="apartment"
                            className={`${styles.inputField} ${getInputClassName('apartment')}`}
                            value={formData.apartment.value}
                            onChange={(e) => handleFieldChange('apartment', e.target.value)}
                            placeholder="Apartment/Suite #"
                        />
                        {formData.apartment.error && (
                            <div className={styles.errorMessage}>
                                {formData.apartment.error}
                            </div>
                        )}
                    </div>

                    <div className={styles.fieldGroup}>
                        <label htmlFor="city">City *</label>
                        <Dropdown
                            value={formData.city.value}
                            onChange={(option) => handleDropdownChange('city', option)}
                            options={cityOptions}
                            placeholder="City *"
                            loading={loadingStates.cities}
                            error={!!formData.city.error}
                            onOpen={() => formData.state.value && loadCities(formData.state.value)}
                        />
                        {formData.city.error && (
                            <div className={styles.errorMessage}>
                                {formData.city.error}
                            </div>
                        )}
                    </div>

                    <div className={styles.fieldGroup}>
                        <label htmlFor="state">State *</label>
                        <Dropdown
                            value={formData.state.value}
                            onChange={(option) => handleDropdownChange('state', option)}
                            options={stateOptions}
                            placeholder="State *"
                            loading={loadingStates.states}
                            error={!!formData.state.error}
                            onOpen={loadStates}
                        />
                        {formData.state.error && (
                            <div className={styles.errorMessage}>
                                {formData.state.error}
                            </div>
                        )}
                    </div>

                    <div className={styles.fieldGroup}>
                        <label htmlFor="zipCode">Zip Code *</label>
                        <Dropdown
                            value={formData.zipCode.value}
                            onChange={(option) => handleDropdownChange('zipCode', option)}
                            options={zipCodeOptions}
                            placeholder="Zip Code *"
                            loading={loadingStates.zipCodes}
                            error={!!formData.zipCode.error}
                            onOpen={() => formData.city.value && loadZipCodes(formData.city.value)}
                        />
                        {formData.zipCode.error && (
                            <div className={styles.errorMessage}>
                                {formData.zipCode.error}
                            </div>
                        )}
                    </div>

                    <div className={styles.fieldGroup}>
                        <div className={styles.helpText}>
                            Enter your phone number for important order updates.
                        </div>
                    </div>

                    <div className={styles.formActions}>
                        <button
                            type="submit"
                            className={styles.submitButton}
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? 'Saving...' : 'Save'}
                        </button>
                        <button
                            type="button"
                            className={styles.cancelButton}
                            onClick={onClose}
                        >
                            Cancel
                        </button>
                    </div>
                </form>
            </div>
        </Popup>
    );
};
