import React from 'react';
import BarChart from '../Graphs/BarChart';

const WeekSalesDisplay = ({ stats, label }) => {
    const data = stats?.graph || [];
    const labels = stats?.labels || [];
    const arrowDirection = stats?.arrow_boolean 
        ? 'M214.6 41.4c-12.5-12.5-32.8-12.5-45.3 0l-160 160c-12.5 12.5-12.5 32.8 0 45.3s32.8 12.5 45.3 0L160 141.2V448c0 17.7 14.3 32 32 32s32-14.3 32-32V141.3l105.4 105.3c12.5 12.5 32.8 12.5 45.3 0s12.5-32.8 0-45.3l-160-160z'
        : 'M169.4 470.6c12.5 12.5 32.8 12.5 45.3 0l160-160c12.5-12.5 12.5-32.8 0-45.3s-32.8-12.5-45.3 0L224 370.8V64c0-17.7-14.3-32-32-32s-32 14.3-32 32v306.7L54.6 265.4c-12.5-12.5-32.8-12.5-45.3 0s-12.5 32.8 0 45.3l160 160z'
    const currency_loc = 'GBP'
    const highestValue = data.length > 0 ? Math.max(...data) : 0;
    
        return (
        <div className='flex-col bg-white rounded-md shadow-md'>
            <div className='flex-col p-4'>
                <div className='text-sm font-medium text-gray-400 text-left'>{label}</div>
                <div className='flex text-left items-center'>
                    <div className='text-black_text font-semibold text-2xl mr-2'>{stats?.count}</div>
                    <svg className='size-5' viewBox='0 0 384 512'>
                        <path d={arrowDirection} />
                    </svg>
                </div>
                <div className='text-left font-medium'>
                    {new Intl.NumberFormat('en-GB', {
                        style: 'currency',
                        currency: currency_loc
                    }).format(stats?.sales ?? 0)}
                </div>
            </div>
            <div className='p-2'>
                <BarChart 
                    xLabels={labels}
                    data={data}
                    chartHeight={300}
                    chartThickness={30}
                    chartStepSize={(Math.round(highestValue / 10) * 10) / 3}
                    showYLabels={false}
                />
            </div>
        </div>
    );
};

export default WeekSalesDisplay