export const InputField = ({
    getInputClassName,
    fieldData,
    validateField,
    fieldName,
    type,
}) => {

    
    return (
        <div className='field'>
            <input
                className={getInputClassName(fieldData)}
                type={type}
                name={fieldName}
                id={fieldName}
                placeholder={fieldName}
                value={fieldData.value}
                onChange={validateField}
                onBlur={validateField}
            />
            <label
                htmlFor={fieldName}
                className={getInputClassName(fieldData)}
            >
                {`${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)}*`}
            </label>
            {fieldData.error && (
                <span className='error'>{fieldData.error}</span>
            )}
        </div>
    );
};
