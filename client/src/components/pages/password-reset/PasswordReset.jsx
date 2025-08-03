import { useParams } from 'react-router';

import { AuthLayout } from '../../reusable/auth-layout/AuthLayout';
import { PasswordResetForm } from './password-reset-form/PasswordResetForm';

import styles from './PasswordReset.module.scss';

export const PasswordReset = () => {
    const { uid, token } = useParams();

    return (
        <AuthLayout>
            <section className={styles['password-reset']}>
                <PasswordResetForm uid={uid} token={token} />
            </section>
        </AuthLayout>
    );
};
