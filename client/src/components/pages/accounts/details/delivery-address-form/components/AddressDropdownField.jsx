import { Dropdown } from '../../../../../reusable/dropdown/Dropdown';

export const AddressDropdownField = ({
    fieldName,
    formData,
    fieldConfig,
    options,
    loading,
    onOpen,
    shouldMakeRequest,
    noOptionsMessage,
    handleDropdownChange,
    getInputClassName
}) => {
    const handleOpen = () => {
        if (shouldMakeRequest && onOpen) {
            onOpen();
        }
    };

    return (
        <Dropdown
            value={formData[fieldName].value}
            onChange={(option) =>
                handleDropdownChange(fieldName, option)
            }
            options={options}
            placeholder={fieldConfig[fieldName].label}
            loading={loading}
            onOpen={handleOpen}
            fieldName={fieldName}
            getInputClassName={getInputClassName}
            fieldData={formData[fieldName]}
            fieldConfig={fieldConfig}
            label={fieldConfig[fieldName].label}
            noOptionsMessage={noOptionsMessage}
        />
    );
};
