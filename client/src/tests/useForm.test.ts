// Comprehensive test for the form system fixes
import { renderHook, act } from '@testing-library/react';
import { useForm } from '../src/hooks/useForm';
import type { UserFormData, FormSubmissionResult } from '../src/types/User';

describe('useForm Hook Fixes', () => {
  const initialFormValues: UserFormData = {
    email: { value: '', error: '', valid: false },
    password: { value: '', error: '', valid: false },
    firstName: { value: '', error: '', valid: false },
    lastName: { value: '', error: '', valid: false },
    phoneNumber: { value: '', error: '', valid: false }
  };

  const mockSubmit = jest.fn(async (formData: UserFormData): Promise<FormSubmissionResult> => {
    return { success: true };
  });

  beforeEach(() => {
    mockSubmit.mockClear();
  });

  test('should not mark fields as valid before user interaction', () => {
    const { result } = renderHook(() => 
      useForm(initialFormValues, { onSubmit: mockSubmit })
    );

    // Initially, no fields should be valid
    expect(result.current.formData.firstName.valid).toBe(false);
    expect(result.current.formData.lastName.valid).toBe(false);
    expect(result.current.formData.email.valid).toBe(false);
    
    // And no fields should be marked as interacted
    expect(result.current.interactedFields.size).toBe(0);
  });

  test('should mark field as valid only after user interaction', async () => {
    const { result } = renderHook(() => 
      useForm(initialFormValues, { onSubmit: mockSubmit })
    );

    // Simulate user typing in first name field
    const changeEvent = {
      target: { name: 'firstName', value: 'John' }
    } as React.ChangeEvent<HTMLInputElement>;

    act(() => {
      result.current.handleFieldChange(changeEvent);
    });

    // Field should have value but not be marked as valid yet (no interaction)
    expect(result.current.formData.firstName.value).toBe('John');
    expect(result.current.formData.firstName.valid).toBe(false);
    expect(result.current.interactedFields.has('firstName')).toBe(false);

    // Simulate blur event (user interaction)
    const blurEvent = {
      target: { name: 'firstName', value: 'John' }
    } as React.FocusEvent<HTMLInputElement>;

    act(() => {
      result.current.validateField(blurEvent);
    });

    // Now field should be marked as interacted and valid
    expect(result.current.formData.firstName.valid).toBe(true);
    expect(result.current.interactedFields.has('firstName')).toBe(true);
  });

  test('should properly handle updateFieldValue without marking as interacted', () => {
    const { result } = renderHook(() => 
      useForm(initialFormValues, { onSubmit: mockSubmit })
    );

    // Simulate loading data from server (like PersonalInfoForm)
    act(() => {
      result.current.updateFieldValue('firstName', 'ServerValue', false);
    });

    // Field should have value but not be marked as valid or interacted
    expect(result.current.formData.firstName.value).toBe('ServerValue');
    expect(result.current.formData.firstName.valid).toBe(false);
    expect(result.current.interactedFields.has('firstName')).toBe(false);
  });

  test('should properly handle updateFieldValue with interaction marking', () => {
    const { result } = renderHook(() => 
      useForm(initialFormValues, { onSubmit: mockSubmit })
    );

    // Simulate updating field and marking as interacted
    act(() => {
      result.current.updateFieldValue('firstName', 'John', true);
    });

    // Field should be marked as valid and interacted
    expect(result.current.formData.firstName.value).toBe('John');
    expect(result.current.formData.firstName.valid).toBe(true);
    expect(result.current.interactedFields.has('firstName')).toBe(true);
  });

  test('should show valid state when typing after field has been interacted with', () => {
    const { result } = renderHook(() => 
      useForm(initialFormValues, { onSubmit: mockSubmit })
    );

    // First interact with field (blur)
    const blurEvent = {
      target: { name: 'firstName', value: 'J' }
    } as React.FocusEvent<HTMLInputElement>;

    act(() => {
      result.current.validateField(blurEvent);
    });

    expect(result.current.interactedFields.has('firstName')).toBe(true);

    // Now type in the field
    const changeEvent = {
      target: { name: 'firstName', value: 'John' }
    } as React.ChangeEvent<HTMLInputElement>;

    act(() => {
      result.current.handleFieldChange(changeEvent);
    });

    // Since field has been interacted with, it should show valid state
    expect(result.current.formData.firstName.value).toBe('John');
    expect(result.current.formData.firstName.valid).toBe(true);
  });

  test('should reset interacted fields when form is reset', () => {
    const { result } = renderHook(() => 
      useForm(initialFormValues, { onSubmit: mockSubmit })
    );

    // Interact with a field
    const blurEvent = {
      target: { name: 'firstName', value: 'John' }
    } as React.FocusEvent<HTMLInputElement>;

    act(() => {
      result.current.validateField(blurEvent);
    });

    expect(result.current.interactedFields.size).toBe(1);

    // Reset form
    act(() => {
      result.current.resetForm();
    });

    // Interacted fields should be cleared
    expect(result.current.interactedFields.size).toBe(0);
    expect(result.current.formData.firstName.value).toBe('');
    expect(result.current.formData.firstName.valid).toBe(false);
  });

  test('should have correct submitAction type', () => {
    const { result } = renderHook(() => 
      useForm(initialFormValues, { onSubmit: mockSubmit })
    );

    // submitAction should be a function that can be passed to form action prop
    expect(typeof result.current.submitAction).toBe('function');
    expect(result.current.submitAction.length).toBe(0); // Should not require parameters
  });
});

// Integration test to verify the PersonalInfoForm fix scenario
describe('PersonalInfoForm Fix Scenario', () => {
  test('should handle server data loading without marking fields as valid', () => {
    const initialFormValues: UserFormData = {
      email: { value: '', error: '', valid: false },
      password: { value: '', error: '', valid: false },
      firstName: { value: '', error: '', valid: false },
      lastName: { value: '', error: '', valid: false },
      phoneNumber: { value: '', error: '', valid: false }
    };

    const { result } = renderHook(() => 
      useForm(initialFormValues, { validateOnSubmit: false })
    );

    // Simulate loading personal info from server (like PersonalInfoForm does)
    act(() => {
      result.current.updateFieldValue('firstName', 'John', false);
      result.current.updateFieldValue('lastName', 'Doe', false);
      result.current.updateFieldValue('phoneNumber', '+1234567890', false);
    });

    // Fields should have values but not be marked as valid (no green styling)
    expect(result.current.formData.firstName.value).toBe('John');
    expect(result.current.formData.firstName.valid).toBe(false);
    
    expect(result.current.formData.lastName.value).toBe('Doe');
    expect(result.current.formData.lastName.valid).toBe(false);
    
    expect(result.current.formData.phoneNumber.value).toBe('+1234567890');
    expect(result.current.formData.phoneNumber.valid).toBe(false);

    // No fields should be marked as interacted
    expect(result.current.interactedFields.size).toBe(0);
  });
});
