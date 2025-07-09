import { Fragment, useState, useCallback } from "react";
import { useNavigate } from "react-router";
import { useUserContext } from "../../../contexts/UserContext";
import { useAuthentication } from "../../../api/authApi";
import { AuthLayout } from "../../reusable/auth-layout/AuthLayout";
import { InputField } from "../../reusable/input-field/InputField";
import { Button } from "../../reusable/button/Button";
import { PasswordValidator } from "../../reusable/password-validator/PasswordValidator";
import { useForm } from "../../../hooks/useForm";
import { FORM_CONFIGS } from "../../../config/formFieldConfigs";
import { createApiDataFromForm } from "../../../utils/formHelpers";

import styles from "./Register.module.scss";
import { Icon } from "../../reusable/icon/Icon";

export const Register = () => {
    const { fieldConfig, initialValues } = FORM_CONFIGS.register;
    const [agree, setAgree] = useState(true);

    const { userLoginHandler } = useUserContext();
    const { register, login } = useAuthentication();
    const navigate = useNavigate();

    const handleSubmit = useCallback(
        async (formData) => {
            const apiData = createApiDataFromForm(formData, fieldConfig);

            const authData = await register(apiData);

            if (authData?.access) {
                userLoginHandler(authData);

                await login({
                    email_or_username: formData.email.value,
                    password: formData.password.value,
                });

                navigate("/my-account/details");
                return { success: true };
            }

            if (authData && typeof authData === "object" && !authData.access) {
                return {
                    success: false,
                    error: "Registration failed",
                    data: authData,
                };
            }

            return {
                success: false,
                error: "Registration failed",
            };
        },
        [fieldConfig, register, userLoginHandler, login, navigate],
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
    } = formProps;

    const navigateToLoginHandler = () => {
        navigate("/my-account/login");
    };

    return (
        <AuthLayout>
            <section className={styles["register"]}>
                <p onClick={navigateToLoginHandler}>
                    <Icon name="arrowLeft" />

                    <span>Back to Sign In</span>
                </p>

                <h2>Create Account</h2>

                <form action={submitAction}>
                    {Object.entries(formData).map(([fieldName, fieldData]) => (
                        <Fragment key={fieldName}>
                            {fieldData && (
                                <InputField
                                    getInputClassName={getInputClassName}
                                    fieldData={fieldData}
                                    handleFieldChange={handleFieldChange}
                                    validateField={validateField}
                                    fieldName={fieldName}
                                    fieldConfig={fieldConfig}
                                />
                            )}
                            {fieldName === "email" && fieldData && (
                                <p>
                                    Enter your email for important order
                                    updates.
                                </p>
                            )}
                            {fieldName === "username" && fieldData && (
                                <p>
                                    Choose a unique username for your account.
                                </p>
                            )}
                        </Fragment>
                    ))}

                    <PasswordValidator
                        password={formData?.password?.value || ""}
                    />

                    <div className={styles["terms-wrapper"]}>
                        <input
                            type="checkbox"
                            name="agree"
                            id="agree"
                            checked={agree}
                            onChange={() => setAgree(!agree)}
                        />
                        <label className={styles["agree"]}>
                            By creating an account, you agree to receive email
                            updates*
                        </label>
                    </div>

                    <Button
                        title={"Register"}
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
