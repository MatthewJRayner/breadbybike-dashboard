import React, { useState } from 'react';
import ShopifyOrdersProvider from '../components/ShopifyOrdersProvider';

function Orders() {
    const [orders, setOrders] = useState([]);

    return (
        <>
            <ShopifyOrdersProvider onOrdersLoaded={setOrders} />
            
            <div>
                {orders.length > 0 ? (
                    <ul>
                        {orders.map(order => (
                            <li key={order.order_id}>
                                {order.customer_name_first} – {order.delivery_date}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p>No orders found.</p>
                )}
            </div>
        </>
    );
}

export default Orders;