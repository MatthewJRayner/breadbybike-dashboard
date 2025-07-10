import React, { useState } from 'react';
import Selector from '../Selector';

const BestSellers = ({stats}) => {
    const [selectedDay, setSelectedDay] = useState('Yesterday');
    const dateKey = selectedDay.toLowerCase().replace(/\s+/g, '_');
    const data = stats?.[dateKey] || [];
    var currency_loc = 'GBP'

    const BestSellerStats = data.names?.map((_, i) => ({
        name: data.names[i],
        sales: data.sales[i],
        count: data.counts[i],
        percentage: data.percentages[i]
    })) || [];

    return (
        <div className='rounded-md shadow-md flex-col bg-white p-4'>
            <div className='flex justify-between items-center'>
                <div className='font-medium text-base text-gray-400'>Best Sellers</div>
                <div className='text-sm'>
                    <Selector
                        label='Period: '
                        value={selectedDay}
                        options={['Yesterday', 'Last Week']}
                        onChange={setSelectedDay}
                    />
                </div>
            </div>
            <div className='mt-2'>
                {BestSellerStats.map((stat, idx) => (
                    <div key={idx} className='flex w-full justify-between items-center mt-3'>
                        <div className='flex items-center'>
                            <h1 className='mr-2 text-lg font-semibold text-black_text'>{stat.name}</h1>
                            <div className='flex items-center font-normal'>
                                <h3 className='mr-2 text-sm font-normal'>
                                    {new Intl.NumberFormat('en-GB', {
                                        style: 'currency',
                                        currency: currency_loc,
                                        minimumFractionDigits: 2
                                    }).format(stat.sales ?? 0)}
                                </h3>
                                <p className='text-xs font-medium text-gray-500'>{stat.count}</p>
                            </div>
                        </div>
                        <div className='text-bbb-blue-500 mr-10 font-semibold'>
                            {stat.percentage}%
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default BestSellers;