import { useState, useEffect } from 'react';
import { useOrder } from '../../../../api/orderApi';
import { ShadowBox } from '../../../reusable/shadow-box/ShadowBox';
import { OrderProductItem } from '../../../reusable/order-product-item/OrderProductItem';
import { formatPrice } from '../../../../utils/formatPrice';
import {
    formatOrderDate,
    formatShortOrderId
} from '../../../../utils/dateHelpers';
import styles from './OrderHistory.module.scss';
import { EmptyList } from '../../../reusable/empty-list/EmptyList';
import { PaddedContainer } from '../../../reusable/padded-container/PaddedContainer';

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

                                <div
                                    className={
                                        styles['order-list']
                                    }
                                >
                                    {orders.map((order) => (
                                        <div
                                            key={order.orderGroup}
                                            className={
                                                styles[
                                                    'order-item'
                                                ]
                                            }
                                        >
                                            <ul
                                                className={
                                                    styles[
                                                        'wrapper-outer'
                                                    ]
                                                }
                                            >
                                                <li
                                                    key={`order-id-${order.orderGroup}`}
                                                >
                                                    <span>
                                                        Order ID
                                                    </span>
                                                    <span>
                                                        {`#${formatShortOrderId(
                                                            order.orderGroup
                                                        )}`}
                                                    </span>
                                                </li>
                                                <li
                                                    key={`order-value-${order.orderGroup}`}
                                                >
                                                    <span>
                                                        Order
                                                        Value
                                                    </span>
                                                    <span>
                                                        {formatPrice(
                                                            order.totalPrice.toString()
                                                        )}
                                                    </span>
                                                </li>
                                                <li
                                                    key={`order-date-${order.orderGroup}`}
                                                >
                                                    <span>
                                                        Order Date
                                                    </span>
                                                    <span>
                                                        {formatOrderDate(
                                                            order.createdAt
                                                        )}
                                                    </span>
                                                </li>
                                                <li
                                                    key={`order-status-${order.orderGroup}`}
                                                >
                                                    <span>
                                                        Order
                                                        Status
                                                    </span>
                                                    <span>
                                                        {order.status ===
                                                        'PE'
                                                            ? 'Pending'
                                                            : 'Completed'}
                                                    </span>
                                                </li>
                                            </ul>

                                            <ShadowBox>
                                                <div
                                                    className={
                                                        styles[
                                                            'products-container'
                                                        ]
                                                    }
                                                >
                                                    <h3>
                                                        Products
                                                        in this
                                                        order
                                                    </h3>
                                                    <div
                                                        className={
                                                            styles[
                                                                'products-grid'
                                                            ]
                                                        }
                                                    >
                                                        {order.products.map(
                                                            (
                                                                product,
                                                                index
                                                            ) => (
                                                                <OrderProductItem
                                                                    key={`${order.orderGroup}-${product.id}-${index}`}
                                                                    product={
                                                                        product
                                                                    }
                                                                />
                                                            )
                                                        )}
                                                    </div>
                                                </div>
                                            </ShadowBox>
                                        </div>
                                    ))}
                                </div>
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
