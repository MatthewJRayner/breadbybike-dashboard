import React from 'react';

const DailyAverage = ({ label, count, percent1, percent2 }) => {
    const isPositive1 = percent1 >= 0
    const isPositive2 = percent2 >= 0
    const percent1Colour = isPositive1
        ? 'text-green-700'
        : 'text-red-700'
    const percent2Colour = isPositive2
        ? 'text-green-700'
        : 'text-red-700'

    return (
        <div className='bg-white flex justify-between items-center p-4 rounded-md shadow-md'>
            <div className='flex-col text-left'>
                <div className='text-xl font-semibold text-black_text mb-1'>{count ?? 0}</div>
                <div className='text-xs text-gray-400 font-normal'>{label}</div>
            </div>
            <div className='flex'>
                <div className={`${percent1Colour} mr-2`}>
                    {isPositive1 ? '+' : ''}
                    {new Intl.NumberFormat('en-GB', {
                        style: 'decimal',
                        maximumFractionDigits: 0
                    }).format(percent1 ?? 0)}%
                </div>
                <div className={`${percent2Colour}`}>
                    {isPositive2 ? '+' : ''}
                    {new Intl.NumberFormat('en-GB', {
                        style: 'decimal',
                        maximumFractionDigits: 0
                    }).format(percent2 ?? 0)}%
                </div>
            </div>
        </div>
    );
};

export default DailyAverage