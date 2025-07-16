import React, { useState } from 'react';
import ShopifyOrdersProvider from '../components/ShopifyOrdersProvider';

function Orders() {
    const [shopifyOrders, setShopifyOrders] = useState([]);

    return (
        <>
            <ShopifyOrdersProvider onOrdersLoaded={setShopifyOrders} />
            
            <div>
                {shopifyOrders.length > 0 ? (
                    <ul>
                        {shopifyOrders.map(order => (
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