import type { ReactElement } from 'react';
import { useForm } from '../../hooks/useForm';
import type { FormData, FormSubmissionResult } from '../../types/User';

interface FormWrapperProps<T extends FormData> {
  initialValues: T;
  onSubmit: (formData: T) => Promise<FormSubmissionResult>;
  children: (formProps: ReturnType<typeof useForm<T>>) => ReactElement;
  validateOnSubmit?: boolean;
  resetOnSuccess?: boolean;
}

/**
 * Higher-order component that provides common form functionality
 * Uses the render prop pattern to give flexibility to the consuming component
 */
export const FormWrapper = <T extends FormData>({
  initialValues,
  onSubmit,
  children,
  validateOnSubmit = true,
  resetOnSuccess = false
}: FormWrapperProps<T>): ReactElement => {
  const formProps = useForm(initialValues, {
    onSubmit,
    validateOnSubmit,
    resetOnSuccess
  });

  return (
    <form action={formProps.submitAction}>
      {children(formProps)}
    </form>
  );
};
