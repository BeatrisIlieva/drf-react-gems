import { ShadowBox } from '../../../../reusable/shadow-box/ShadowBox';
import { OrderProductItem } from './order-product-item/OrderProductItem';

import { formatOrderDate, formatShortOrderId } from '../../../../../utils/dateHelpers';
import { formatPrice } from '../../../../../utils/formatPrice';

import styles from './OrderList.module.scss';

export const OrderList = ({ orders }) => {
    return (
        <div className={styles['order-list']}>
            {orders.map(order => (
                <div key={order.orderGroup} className={styles['order-item']}>
                    <ul className={styles['wrapper-outer']}>
                        <li key={`order-id-${order.orderGroup}`}>
                            <span>Order ID</span>
                            <span>{`#${formatShortOrderId(order.orderGroup)}`}</span>
                        </li>
                        <li key={`order-value-${order.orderGroup}`}>
                            <span>Order Value</span>
                            <span>{formatPrice(order.totalPrice.toString())}</span>
                        </li>
                        <li key={`order-date-${order.orderGroup}`}>
                            <span>Order Date</span>
                            <span>{formatOrderDate(order.createdAt)}</span>
                        </li>
                        <li key={`order-status-${order.orderGroup}`}>
                            <span>Order Status</span>
                            <span>{order.status === 'PE' ? 'Pending' : 'Completed'}</span>
                        </li>
                    </ul>

                    <ShadowBox>
                        <div className={styles['products-container']}>
                            <h3>Products in this order</h3>
                            <div className={styles['products-grid']}>
                                {order.products.map((product, index) => (
                                    <OrderProductItem
                                        key={`${order.orderGroup}-${product.id}-${index}`}
                                        product={product}
                                    />
                                ))}
                            </div>
                        </div>
                    </ShadowBox>
                </div>
            ))}
        </div>
    );
};
