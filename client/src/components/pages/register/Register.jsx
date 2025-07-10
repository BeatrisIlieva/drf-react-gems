import { useNavigate } from 'react-router';

import { AuthLayout } from '../../reusable/auth-layout/AuthLayout';
import { Button } from '../../reusable/button/Button';
import { Icon } from '../../reusable/icon/Icon';
import { InputField } from '../../reusable/input-field/InputField';
import { PasswordValidator } from '../../reusable/password-validator/PasswordValidator';
import { Agreement } from './agreement/Agreement';
import { FieldHelp } from './field-help/FieldHelp';

import { useForm } from '../../../hooks/useForm';
import { useRegister } from '../../../hooks/useRegister';

import { FORM_CONFIGS } from '../../../config/formFieldConfigs';

import styles from './Register.module.scss';

export const Register = () => {
    const navigate = useNavigate();
    const { fieldConfig, initialValues } = FORM_CONFIGS.register;

    const { handleSubmit, agree, agreeError, toggleAgreement, validateAgreement } =
        useRegister(fieldConfig);

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
    } = formProps;

    const handleFormSubmit = e => {
        if (!validateAgreement()) {
            e.preventDefault();
        }
    };

    return (
        <AuthLayout>
            <section className={styles['register']}>
                <p onClick={() => navigate('/my-account/login')}>
                    <Icon name="arrowLeft" />
                    <span>Back to Sign In</span>
                </p>

                <h2>Create Account</h2>

                <form action={submitAction} onSubmit={handleFormSubmit}>
                    {Object.entries(formData).map(
                        ([fieldName, fieldData]) =>
                            fieldData && (
                                <div key={fieldName}>
                                    <InputField
                                        getInputClassName={getInputClassName}
                                        fieldData={fieldData}
                                        handleFieldChange={handleFieldChange}
                                        validateField={validateField}
                                        fieldName={fieldName}
                                        fieldConfig={fieldConfig}
                                    />
                                    <FieldHelp
                                        fieldName={fieldName}
                                        show={fieldName === 'email' || fieldName === 'username'}
                                    />
                                </div>
                            )
                    )}

                    <PasswordValidator password={formData?.password?.value || ''} />

                    <Agreement agree={agree} agreeError={agreeError} onToggle={toggleAgreement} />

                    <Button
                        title="Register"
                        color="black"
                        actionType="submit"
                        pending={isSubmitting}
                        success={formProps.formState?.success}
                        callbackHandler={() => {}}
                    />
                </form>
            </section>
        </AuthLayout>
    );
};
