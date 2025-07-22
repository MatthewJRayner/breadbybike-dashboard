import React, { useState } from 'react';
import ShopifyOrdersProvider from '../components/ShopifyOrdersProvider';
import OrdersDisplay from '../components/OrdersDisplay';
import useRequireAccessLevel from '../components/requireAccessLevel';

function Orders() {
    useRequireAccessLevel('staff')

    const [orders, setOrders] = useState([]);
    const today = new Date().toISOString().split('T')[0];
    const todaysOrders = orders.filter(o => o.delivery_date === today);
    const futureOrders = orders.filter(o => o.delivery_date > today);

    return (
        <div className='flex-col w-full'>
            <ShopifyOrdersProvider onOrdersLoaded={setOrders} />
            <div className="bg-white shadow-md flex p-4 pt-5 pb-5 rounded-2xl text-md items-center w-full">
                <h1 className="text-gray-300 mr-4 md:mr-8 inline-block"><span className='text-black_text hidden md:inline-block'>BBB Dashboard </span> <span className='hidden md:inline-block'> | </span><span className='text-black_text md:text-gray-300 font-semibold md:font-normal'> Orders</span></h1>
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