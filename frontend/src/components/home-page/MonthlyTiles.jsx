import React from 'react';

const MonthlyTiles = ({ stats }) => {
    return (
        <div className='grid grid-cols-2 mt-4 w-full'>
            {Array.isArray(stats) && stats.length > 0 ? (
                stats.map((stat, idx) => {
                    const isSpecial = idx === 1 || idx === 2;
                    const containerClasses = isSpecial
                        ? 'bg-bbb-blue-500 text-white'
                        : 'bg-white text-black-text'
                    
                    const iconClasses = isSpecial
                        ? 'fill-white'
                        : 'fill-bbb-blue-500'
                    
                    const isLeft = idx === 0 || idx === 2;
                    const marginClass = isLeft
                        ? 'mr-2'
                        : 'ml-2'

                    return (
                        <div key={idx} className={`${containerClasses} ${marginClass} rounded-lg shadow-mdflex justify-between items-center flex p-4 mb-4`}>
                        <div className='flex-col text-left'>
                            <div className='text-sm text-gray-400 font-thing'>{stat.label}</div>
                            <div className='font-semibold'>
                                {stat.currency || ''}{new Intl.NumberFormat('en-UK', {
                                    style: 'decimal',
                                    minimumFractionDigits: 0,
                                    maximumFractionDigits: 2,
                                }).format(stat.value ?? 0)}
                            </div>
                        </div>
                        <div>
                            <svg className={`${iconClasses} size-5`} viewBox={stat.viewbox}>
                                <path d={stat.icon_path} />
                            </svg>
                        </div>
                    </div>
                    );
                })
            ) : (
                <p className="text-gray-400 text-sm">Loading summary...</p>
            )}
        </div>
    );
};

export default MonthlyTiles