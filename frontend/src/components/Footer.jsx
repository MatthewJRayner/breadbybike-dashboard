import React from 'react';

function Footer() {
    const current_year = new Date().toLocaleDateString('en-US', { year: 'numeric' })

    return (
        <div className='text-gray-500'><span className='font-medium'>Matthew Rayner</span> | {current_year}</div>
    );
};

export default Footer;