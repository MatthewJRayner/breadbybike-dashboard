import React from 'react';

const DailyStatsSummary = ({stats}) => {
    return (
        <div className="grid grid-cols-2 sm:grid-cols-3 bg-white pt-6 pl-6 pr-4 rounded-md shadow-md w-full">
            {Array.isArray(stats) && stats.length > 0 ? (
                stats.map((stat, idx) => {
                    const isCurrency = Boolean(stat.currency);
                    const formattedValue = new Intl.NumberFormat('en-UK', {
                        style: 'decimal',
                        minimumFractionDigits: isCurrency ? 2 : 0,
                        maximumFractionDigits: 2,
                    }).format(stat.value ?? 0);
                    
                    return (
                        <div key={idx} className="flex items-center text-center mb-6">
                            <div className="text-bbb-blue-600 w-1/5">
                                <svg className='size-5 fill-current' viewBox={stat.viewbox}>
                                    <path d={stat.icon_path} />
                                </svg>
                            </div>
                            <div className='w-4/5 pr-2 sm:pr-4 ml-2 sm:ml-0'> 
                                <div className="text-sm sm:text-md font-semibold text-black_text">
                                    {stat.currency || ''}
                                    {formattedValue}
                                </div>
                                <div className="text-gray-400 font-normal text-[8px] sm:text-[11px]">{stat.label}</div>
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

export default DailyStatsSummary