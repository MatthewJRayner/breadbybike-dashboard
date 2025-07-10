import React from 'react';

const StatsBlock = ({ label, value, percentage}) => {
    const isPositive = percentage >= 0
    const percentageColour = isPositive
        ? 'text-green-700'
        : 'text-red-700'

    return (
        <div className='bg-white rounded-md shadow-md flex justify-between items-center w-full p-4'>
            <div className='flex-col text-left'>
                <div className='font-semibold text-black_text text-xl'>
                    {new Intl.NumberFormat('en-GB', {
                        style: 'currency',
                        currency: 'GBP',
                        minimumFractionDigits: 2,
                    }).format(value ?? 0)}
                </div>
                <div className='text-sm font-normal text-gray-400'>{label}</div>
            </div>
            <div className={`${percentageColour} font-normal text-lg`}>
                {isPositive ? '+' : ''}
                {new Intl.NumberFormat('en-GB', {
                    style: 'decimal',
                    maximumFractionDigits: 0
                }).format(percentage ?? 0)}%
            </div>
        </div>
    );
};

export default StatsBlock