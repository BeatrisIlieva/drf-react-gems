import { useEffect, useState } from 'react';

import { EmptyList } from '../../../reusable/empty-list/EmptyList';
import { PaddedContainer } from '../../../reusable/padded-container/PaddedContainer';
import { OrderList } from './order-list/OrderList';

import { useOrder } from '../../../../api/orderApi';

import styles from './OrderHistory.module.scss';

export const OrderHistory = () => {
    const { getOrders } = useOrder();

    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchOrders = async () => {
            setLoading(true);
            try {
                const response = await getOrders();
                if (response && response.results) {
                    setOrders(response.results);
                } else if (Array.isArray(response)) {
                    setOrders(response);
                }
            } catch (err) {
                console.error(err instanceof Error ? err.message : String(err));
                setOrders([]);
            } finally {
                setLoading(false);
            }
        };

        fetchOrders();
    }, [getOrders]);

    return (
        <>
            {!loading && (
                <>
                    {orders.length > 0 ? (
                        <PaddedContainer>
                            <section className={styles['order-history']}>
                                <h2>Order History</h2>

                                <OrderList orders={orders} />
                            </section>
                        </PaddedContainer>
                    ) : (
                        <EmptyList title="You have no orders yet." />
                    )}
                </>
            )}
        </>
    );
};
