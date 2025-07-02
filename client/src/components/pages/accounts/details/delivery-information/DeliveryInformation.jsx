import { useMemo } from 'react';
import { DetailsContainer } from '../details-container/DetailsContainer';
import { useUserAddress } from '../../../../../api/accounts/userAddressApi';

export const DeliveryInformation = () => {
    const initialFormValues = useMemo(
        () => ({
            apartment: { value: '', error: '', valid: false }, // Required by UserFormData
            state: { value: '', error: '', valid: false }, // Required by UserFormData
            city: { value: '', error: '', valid: false },
            streetAddress: { value: '', error: '', valid: false },
            zipCode: { value: '', error: '', valid: false }
        }),
        []
    );

    const {
        getUserAddress,
        updateUserAddress,
        deleteUserAddress,
        getStates,
        getCities,
        getZipCodes,
        getStreetAddresses
    } = useUserAddress();
    return (
        <DetailsContainer>
            <h3>Delivery Information</h3>
        </DetailsContainer>
    );
};
