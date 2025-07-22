import React from 'react';

const Selector = ({ label, value, options, onChange }) => {
    return (
        <div className='sm:pr-3 sm:pl-3 text-black_text flex items-center max-w-full'>
            <label htmlFor={`${label}-select`} className='mr-2 hidden lg:block whitespace-nowrap'>{label}</label>
            <select 
                id={`${label}-select`} 
                value={value} 
                onChange={(e) => onChange(e.target.value)}
                title={value}
                className="text-bbb-blue-100 p-1 pl-2 pr-2 border border-background_grey rounded-lg shadow-md bg-bbb-blue-500 focus:ring-background_grey focus:border-background_grey max-w-[85px] sm:max-w-[180px] overflow-hidden text-ellipsis whitespace-nowrap truncate"
            >
                {options.map((option) => (
                    <option key={option} value={option}>{option}</option>
                ))}
            </select>
        </div>
    );
};

export default Selector