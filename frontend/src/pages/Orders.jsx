import React, { useState } from 'react';
import ShopifyOrdersProvider from '../components/ShopifyOrdersProvider';
import OrdersDisplay from '../components/OrdersDisplay';

function Orders() {
    const [orders, setOrders] = useState([]);

    const today = new Date().toISOString().split('T')[0];
    const todaysOrders = orders.filter(o => o.delivery_date === today);
    const futureOrders = orders.filter(o => o.delivery_date > today);

    return (
        <div className='flex-col w-full'>
            <ShopifyOrdersProvider onOrdersLoaded={setOrders} />
            <div className="bg-white shadow-md flex p-4 pt-5 pb-5 rounded-2xl text-md items-center w-full">
                <h1 className="text-black_text mr-12">BBB Dashboard <span className="text-gray-300"> | Orders</span></h1>
            </div>
            <div className='mt-4'>
                <OrdersDisplay orders={todaysOrders} title={`Today`}/>
            </div>
            <div className='mt-4'>
                <OrdersDisplay orders={futureOrders} title={`Upcoming`}/>
            </div>
        </div>
    );
}

export default Orders;