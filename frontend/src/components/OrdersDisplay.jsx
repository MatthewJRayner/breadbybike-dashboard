import React from 'react';

const OrdersDisplay = ({ orders, title, maxHeight = null }) => {
    return (
        <div className='w-full bg-white rounded-md shadow-md flex-col text-left p-4' style={maxHeight ? { maxHeight, overflowY: 'auto' } : {}}>
            <div className='text-black_text font-medium text-md sm:text-lg md:text-2xl'>{title.toUpperCase()}</div>

            {orders.length === 0 ? (
                <div className='text-bbb-blue-200 text-sm md:text-md text-normal font-medium italic mt-2'>No orders found.</div>
            ) : (
                <div className='flex flex-col sm:flex-row max-w-full text-sm md:text-md'>
                    <div className='text-left w-full sm:w-fit mr-10'>
                        <div className='text-bbb-blue-400 font-medium'>Order No.</div>
                        {orders.map((order, idx) => (
                            <div className='mt-2' key={idx}>{order.order_id}</div>
                        ))}
                    </div>
                    <div className='text-left w-full sm:w-fit mr-10'>
                        <div className='text-bbb-blue-400 font-medium'>Name</div>
                        {orders.map((order, idx) => (
                            <div className='mt-2' key={idx}>{order.customer_name_first} {`${order.customer_name_last}`}</div>
                        ))}
                    </div>
                    <div className='text-left w-full sm:w-fit mr-10'>
                        <div className='text-bbb-blue-400 font-medium'>Items</div>
                        {orders.map((order, idx) => (
                            <div key={idx}>
                                {order.line_items.map((item, i) => (
                                    <div className='mt-2' key={i}>{item.title} x {item.current_quantity}</div>
                                ))}
                            </div>
                        ))}
                    </div>
                    <div className='text-left w-full sm:w-fit mr-10'>
                        <div className='text-bbb-blue-400 font-medium'>Date</div>
                        {orders.map((order, idx) => (
                            <div className='mt-2' key={idx}>{order.delivery_date}</div>
                        ))}
                    </div>
                    <div className='text-left w-full sm:w-fit mr-10'>
                        <div className='text-bbb-blue-400 font-medium'>Note</div>
                        {orders.map((order, idx) => (
                            <div key={idx} className={order.notes ? 'font-semibold text-black_text mt-2' : 'text-gray-400 mt-2'}>
                                {order.notes || `No note attached`}
                            </div>
                        ))}
                        
                    </div>
                </div>
            )}
        </div>
    );
};

export default OrdersDisplay