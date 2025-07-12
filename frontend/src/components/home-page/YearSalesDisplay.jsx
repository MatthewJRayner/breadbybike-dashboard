import React from 'react';
import BarChart from '../Graphs/BarChart';

const YearSalesDisplay = ({ stats, title, label1, label2, height }) => {
    const labels = stats?.labels || [];
    const data = Object.values(stats?.graph || {});
    var currency_loc = 'GBP'

    // Dynamic calculation for the thickness of bars
    const numBars = labels.length;
    const baseThickness = 40;
    const minThickness = 10;
    const maxBars = 12;
    const chartThickness = Math.max(
        minThickness,
        Math.min(baseThickness, baseThickness * (maxBars / Math.max(numBars, 1)))
    );

    return (
        <div className='bg-white flex-col rounded-md shadow-md text-left p-4'>
            <div className='mb-2 text-gray-400 text-sm font-medium'>
                {title}
            </div>
            <div className='flex mb-4 items-center'>
                <div className='flex-col mr-4 justify-center items-center'>
                    <div className='text-lg text-black_text font-semibold'>
                        {new Intl.NumberFormat('en-GB', {
                            style: 'currency',
                            currency: currency_loc
                        }).format(stats?.total_sales_year ?? 0)}
                    </div>
                    <div className='text-sm text-gray-400'>{label1}</div>
                </div>
                <div className='flex-col'>
                    <div className='text-lg text-black_text font-semibold'>
                        {new Intl.NumberFormat('en-GB', {
                            style: 'currency',
                            currency: currency_loc
                        }).format(stats?.monthly_average ?? 0)}
                    </div>
                    <div className='text-sm text-gray-400'>{label2}</div>
                </div>
            </div>
            <div>
                <BarChart 
                    xLabels={labels}
                    data={data}
                    chartHeight={height}
                    chartThickness={chartThickness}
                    currency={true}
                    chartStepSize={Math.round((stats?.monthly_average / 3) / 10000) * 10000}
                />
            </div>
        </div>
    );
};

export default YearSalesDisplay;