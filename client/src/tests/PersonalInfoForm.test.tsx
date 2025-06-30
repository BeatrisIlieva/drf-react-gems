import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { PersonalInfoForm } from '../components/pages/accounts/details/personal-info-form/PersonalInfoForm';

// Mock the API hooks
const mockGetPersonalInfo = jest.fn();
const mockUpdatePersonalInfo = jest.fn();

jest.mock('../api/authApi', () => ({
    useGetPersonalInfo: () => ({ getPersonalInfo: mockGetPersonalInfo }),
    useUpdatePersonalInfo: () => ({ updatePersonalInfo: mockUpdatePersonalInfo })
}));

describe('PersonalInfoForm Validation', () => {
    beforeEach(() => {
        mockGetPersonalInfo.mockClear();
        mockUpdatePersonalInfo.mockClear();
        mockGetPersonalInfo.mockResolvedValue(null);
    });

    it('should require all fields to be filled', async () => {
        render(<PersonalInfoForm />);
        
        // Wait for form to load
        await waitFor(() => {
            expect(screen.getByText('Personal Information')).toBeInTheDocument();
        });

        const saveButton = screen.getByRole('button', { name: /save changes/i });
        
        // Try to submit empty form
        fireEvent.click(saveButton);

        // Should show validation errors for all fields
        await waitFor(() => {
            expect(screen.getAllByText('This field is required')).toHaveLength(3);
        });
    });

    it('should validate firstName format', async () => {
        render(<PersonalInfoForm />);
        
        await waitFor(() => {
            expect(screen.getByText('Personal Information')).toBeInTheDocument();
        });

        const firstNameInput = screen.getByLabelText(/first name/i);
        
        // Enter invalid first name (with numbers)
        fireEvent.change(firstNameInput, { target: { value: 'John123' } });
        fireEvent.blur(firstNameInput);

        await waitFor(() => {
            expect(screen.getByText('Name must contain only letters and be 2-30 characters long')).toBeInTheDocument();
        });
    });

    it('should validate lastName format', async () => {
        render(<PersonalInfoForm />);
        
        await waitFor(() => {
            expect(screen.getByText('Personal Information')).toBeInTheDocument();
        });

        const lastNameInput = screen.getByLabelText(/last name/i);
        
        // Enter invalid last name (too short)
        fireEvent.change(lastNameInput, { target: { value: 'D' } });
        fireEvent.blur(lastNameInput);

        await waitFor(() => {
            expect(screen.getByText('Name must contain only letters and be 2-30 characters long')).toBeInTheDocument();
        });
    });

    it('should validate phoneNumber format', async () => {
        render(<PersonalInfoForm />);
        
        await waitFor(() => {
            expect(screen.getByText('Personal Information')).toBeInTheDocument();
        });

        const phoneInput = screen.getByLabelText(/phone number/i);
        
        // Enter invalid phone number (too short)
        fireEvent.change(phoneInput, { target: { value: '123' } });
        fireEvent.blur(phoneInput);

        await waitFor(() => {
            expect(screen.getByText('Phone number must be 9-15 digits long')).toBeInTheDocument();
        });
    });

    it('should prevent submission with invalid data', async () => {
        render(<PersonalInfoForm />);
        
        await waitFor(() => {
            expect(screen.getByText('Personal Information')).toBeInTheDocument();
        });

        // Fill form with invalid data
        fireEvent.change(screen.getByLabelText(/first name/i), { target: { value: 'John123' } });
        fireEvent.change(screen.getByLabelText(/last name/i), { target: { value: 'D' } });
        fireEvent.change(screen.getByLabelText(/phone number/i), { target: { value: '123' } });

        const saveButton = screen.getByRole('button', { name: /save changes/i });
        fireEvent.click(saveButton);

        // Should not call API with invalid data
        await waitFor(() => {
            expect(mockUpdatePersonalInfo).not.toHaveBeenCalled();
        });
    });

    it('should submit successfully with valid data', async () => {
        mockUpdatePersonalInfo.mockResolvedValue({ success: true });
        
        render(<PersonalInfoForm />);
        
        await waitFor(() => {
            expect(screen.getByText('Personal Information')).toBeInTheDocument();
        });

        // Fill form with valid data
        fireEvent.change(screen.getByLabelText(/first name/i), { target: { value: 'John' } });
        fireEvent.change(screen.getByLabelText(/last name/i), { target: { value: 'Doe' } });
        fireEvent.change(screen.getByLabelText(/phone number/i), { target: { value: '1234567890' } });

        const saveButton = screen.getByRole('button', { name: /save changes/i });
        fireEvent.click(saveButton);

        // Should call API with valid data
        await waitFor(() => {
            expect(mockUpdatePersonalInfo).toHaveBeenCalledWith({
                first_name: 'John',
                last_name: 'Doe',
                phone_number: '1234567890'
            });
        });
    });

    it('should show "This field is required" for empty fields', async () => {
        render(<PersonalInfoForm />);
        
        await waitFor(() => {
            expect(screen.getByText('Personal Information')).toBeInTheDocument();
        });

        const firstNameInput = screen.getByLabelText(/first name/i);
        
        // Focus and blur empty field
        fireEvent.focus(firstNameInput);
        fireEvent.blur(firstNameInput);

        await waitFor(() => {
            expect(screen.getByText('This field is required')).toBeInTheDocument();
        });
    });
});
