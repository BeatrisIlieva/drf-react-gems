import { useState, useEffect } from 'react';
import { useOrder } from '../../../../api/orderApi';
import styles from './OrderHistory.module.scss';
import { EmptyList } from '../../../reusable/empty-list/EmptyList';
import { PaddedContainer } from '../../../reusable/padded-container/PaddedContainer';
import { OrderList } from './order-list/OrderList';

export const OrderHistory = () => {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);
    const { getOrders } = useOrder();

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
                console.error(
                    err instanceof Error
                        ? err.message
                        : String(err)
                );
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
                            <section
                                className={
                                    styles['order-history']
                                }
                            >
                                <h2>Order History</h2>

                                <OrderList orders={orders} />
                            </section>
                        </PaddedContainer>
                    ) : (
                        <EmptyList title='Order History' />
                    )}
                </>
            )}
        </>
    );
};
