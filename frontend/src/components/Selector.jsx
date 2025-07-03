import React from 'react';

const Selector = ({ label, value, options, onChange }) => {
    return (
        <div className='pr-3 pl-3 text-black_text flex items-center'>
            <label htmlFor={`${label}-select`} className='mr-2'>{label}</label>
            <select 
                id={`${label}-select`} 
                value={value} 
                onChange={(e) => onChange(e.target.value)}
                title=""
                className="justify-center text-bbb-blue-100 w-auto max-w-xs p-1 pl-2 pr-2 border border-background_grey rounded-lg shadow-sm bg-bbb-blue-500 focus:ring-background_grey focus:border-background_grey max-h-20 overflow-y-auto"
            >
                {options.map((option) => (
                    <option key={option} value={option}>{option}</option>
                ))}
            </select>
        </div>
    );
};

export default Selector