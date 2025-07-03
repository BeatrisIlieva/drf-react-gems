import { AddressDropdownField } from './AddressDropdownField';

export const AddressDropdownGroup = ({
    formData,
    fieldConfig,
    stateOptions,
    cityOptions,
    zipCodeOptions,
    loadingStates,
    loadStates,
    loadCities,
    loadZipCodes,
    handleDropdownChange,
    getInputClassName
}) => {
    const dropdownFields = [
        {
            fieldName: 'state',
            options: stateOptions,
            loading: loadingStates.states,
            onOpen: loadStates,
            shouldMakeRequest: true,
            noOptionsMessage: 'No options available'
        },
        {
            fieldName: 'city',
            options: cityOptions,
            loading: loadingStates.cities,
            onOpen: () => {
                if (formData.state.value) {
                    loadCities(formData.state.value);
                }
            },
            shouldMakeRequest: !!formData.state.value,
            noOptionsMessage: 'Please select a State'
        },
        {
            fieldName: 'zipCode',
            options: zipCodeOptions,
            loading: loadingStates.zipCodes,
            onOpen: () => {
                if (formData.city.value) {
                    loadZipCodes(formData.city.value);
                }
            },
            shouldMakeRequest: !!formData.city.value,
            noOptionsMessage: 'Please select a City'
        }
    ];

    return (
        <>
            {dropdownFields.map(({ fieldName, options, loading, onOpen, shouldMakeRequest, noOptionsMessage }) => (
                <AddressDropdownField
                    key={fieldName}
                    fieldName={fieldName}
                    formData={formData}
                    fieldConfig={fieldConfig}
                    options={options}
                    loading={loading}
                    onOpen={onOpen}
                    shouldMakeRequest={shouldMakeRequest}
                    noOptionsMessage={noOptionsMessage}
                    handleDropdownChange={handleDropdownChange}
                    getInputClassName={getInputClassName}
                />
            ))}
        </>
    );
};
