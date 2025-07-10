import React from 'react';

const RecentTime = ({ label, time }) => {
    return (
        <div className='bg-white w-full rounded-md shadow-md p-4 flex justify-between items-center'>
            <div className='text-black_text font-semibold text-xl'>{time?.slice(0, 5) ?? '08:00'}</div>
            <div className='text-gray-400'>{label}</div>
        </div>
    );
};

export default RecentTime