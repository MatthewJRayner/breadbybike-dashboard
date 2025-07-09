import React from 'react';

const DailyStatsSummary = ({stats}) => {
    return (
        <div className="grid grid-cols-3 bg-white pt-6 pl-4 pr-4 rounded-lg shadow-md mt-4 w-full">
            {Array.isArray(stats) && stats.length > 0 ? (
                stats.map((stat, idx) => (
                    <div key={idx} className="flex items-center text-center mb-6">
                        <div className="text-bbb-blue-600 w-1/5">
                            <svg className='size-5 fill-current' viewBox={stat.viewbox}>
                                <path d={stat.icon_path} />
                            </svg>
                        </div>
                        <div className='w-4/5 pr-4'> 
                            <div className="text-md font-semibold text-black_text">
                                {stat.currency || ''}{new Intl.NumberFormat('en-UK', {
                                    style: 'decimal',
                                    minimumFractionDigits: 0,
                                    maximumFractionDigits: 2,
                                }).format(stat.value ?? 0)}
                            </div>
                            <div className="text-gray-400 font-normal text-[11px]">{stat.label}</div>
                        </div>
                    </div>
                ))
            ) : (
                <p className="text-gray-400 text-sm">Loading summary...</p>
            )}
        </div>
    );
};

export default DailyStatsSummary