import React from 'react';
import BarChart from '../Graphs/BarChart';

const MonthSalesDisplay = ({ stats, label, desc }) => {
    const data = stats?.graph || [];
    const labels = stats?.labels || [];
    const getPercentageColour = (key, defaultValue = 0) => {
        const value = stats?.percentages?.[key] ?? defaultValue;
        return value >= 0 ? 'text-green-700' : 'text-red-700';
    };
    const weekColour = getPercentageColour('previous_month');
    const yearColour = getPercentageColour('previous_year')
    const currency_loc = 'GBP'
    const highestValue = data.length > 0 ? Math.max(...data) : 0;

    return (
        <div className='bg-white rounded-md shadow-md flex-col w-full'>
            <div className='flex-col mb-4 text-left p-4'>
                <div className='flex mb-2 items-center'>
                    <div className='flex-col mr-4'>
                        <div className='text-black_text font-semibold text-md'>
                            {new Intl.NumberFormat('en-GB', {
                                style: 'currency',
                                currency: currency_loc
                            }).format(stats?.total_sales_month ?? 0)}
                        </div>
                        <div className='text-bbb-blue-600 font-semibold text-xs'>{label}</div>
                    </div>
                    <div className='flex-col text-xs text-center font-medium'>
                        <div className={`${weekColour} tooltip-trigger`}>{stats?.percentages?.previous_month}%</div>
                        <div className={`${yearColour}`}>{stats?.percentages?.previous_year}%</div>
                    </div>
                </div>
                <div className='text-gray-400 text-left text-[10px]'>{desc}</div>
            </div>
            <div className='w-full flex'>
                <BarChart 
                    xLabels={labels}
                    data={data}
                    chartHeight={150}
                    currency={true}
                    chartThickness={4}
                    chartStepSize={highestValue + 5}
                    showLabels={false}
                />
            </div>
        </div>
    );
};

export default MonthSalesDisplay